import time

from django.conf import settings
from django.conf.urls import url
from django.db.models import Q

from easy_thumbnails.files import get_thumbnailer

from restless.exceptions import BadRequest, NotFound
from restless.dj import DjangoResource

from courses.models import Course


class CourseResource(DjangoResource):
    def __init__(self, *args, **kwargs):
        super(CourseResource, self).__init__(*args, **kwargs)
        self.http_methods.update({
            'random_course': {
                'GET': 'random_course',
            }
        })
        self.base_qs = Course.approved.all()

    def _get_start(self):
        if not 'start' in self.request.GET:
            return None

        try:
            return int(self.request.GET.get('start', 0))
        except ValueError:
            raise BadRequest("Invalid start parameter.")

    def _get_limit(self):
        try:
            limit = int(self.request.GET.get('limit', 100))
        except ValueError:
            raise BadRequest("Invalid limit parameter.")

        if limit > 1000:
            limit == 1000

        return limit

    def _get_order(self):
        order = self.request.GET.get('order', 'desc')

        if order not in ('asc', 'desc'):
            raise BadRequest("Invalid order parameter.")

        if order == 'asc':
            return 'created'

        return '-created'

    def _apply_filters(self, qs):
        """
        This method takes a `QuerySet` & adds on the various filtering calls.

        It returns a *new* QS, so be sure to store the result & use that rather
        than the QS passed it.
        """
        if 'system' in self.request.GET:
            qs = qs.filter(system__istartswith=self.request.GET['system'])

        if 'course_type' in self.request.GET:
            course_type = self.request.GET['course_type']

            if course_type not in (
                'all', 'zerogravity', 'surface', 'srvrally', 'srvcross',
                'stadium'
            ):
                raise BadRequest("Invalid course_type parameter.")

            if course_type != 'all':
                qs = qs.filter(course_type=course_type)

        if 'created_by' in self.request.GET:
            qs = qs.filter(
                created_by__name__iexact=self.request.GET['created_by']
            )

        if 'vehicle_type' in self.request.GET:
            vehicle_type = self.request.GET['vehicle_type']

            if vehicle_type not in ('all', 'ship', 'srv'):
                raise BadRequest("Invalid vehicle_type parameter.")

            # We're cheating a bit here, since we're not really filtering by
            # the provided value, but since we know what vehicle type applies
            # to what kind of course, this gives a simpler query (though one
            # we'll have to update if/when new course types get added).
            if vehicle_type == 'ship':
                qs = qs.filter(
                    Q(course_type='zerogravity') |
                    Q(course_type='surface') |
                    Q(course_type='stadium')
                )
            elif vehicle_type == 'srv':
                qs = qs.filter(
                    Q(course_type='srvrally') |
                    Q(course_type='srvcross')
                )

        return qs

    def list(self):
        # Apply any provided `GET` filters.
        qs = self._apply_filters(self.base_qs)

        # Check for a starting offset & ordering.
        start = self._get_start()
        order = self._get_order()

        if start is not None:
            qs = qs.filter(pk__gte=start)

        # Apply ordering just before slicing.
        qs = qs.order_by(order)

        # Slice it down to a page-worth.
        limit = self._get_limit()
        return qs[:limit]

    def detail(self, pk):
        return Course.objects.get(id=pk)

    def wrap_list_response(self, data):
        return {
            'meta': {
                'start': self._get_start(),
                'limit': self._get_limit(),
                # Re-apply all the filters to run a count.
                'total': self._apply_filters(self.base_qs).count(),
            },
            'courses': data,
        }

    def make_timestamp(self, dt):
        return int((time.mktime(dt.timetuple()) * 1000) + dt.microsecond)

    def prepare(self, data):
        prepped = {
            "id": data.pk,
            "title": data.title,
            "system": data.system,
            "course_type": data.course_type,
            "nearby_outfitting": data.nearby_outfitting,
            "distance_from_primary": data.distance_from_primary,
            "distance_from_sol": data.distance_from_sol,
            "notes": data.notes,
            "screenshots": [],
            "created_by": data.created_by.name,
            # The timestamp in milliseconds
            "created": self.make_timestamp(data.created),
            "url": data.get_absolute_url(),
        }

        thumb_opts = settings.THUMBNAIL_ALIASES['courses.CourseScreenshot.shot']['primary_thumbnail']

        for screenshot in data.screenshots.all():
            thumb_url = get_thumbnailer(screenshot.shot).get_thumbnail(thumb_opts).url
            prepped['screenshots'].append({
                'fullsize': screenshot.shot.url,
                'thumbnail': thumb_url,
            })

        if data.course_type == Course.COURSE_ZEROGRAVITY:
            prepped['course_info'] = {
                "vehicle_type": data.zerogravitycourse.vehicle_type,
                "station_name": data.zerogravitycourse.station_name,
                "number_of_rings": data.zerogravitycourse.number_of_rings,
                "length": data.zerogravitycourse.length,
            }
        elif data.course_type == Course.COURSE_SURFACE:
            prepped['course_info'] = {
                "vehicle_type": data.surfacecourse.vehicle_type,
                "planet_name": data.surfacecourse.planet_name,
                "coordinates": data.surfacecourse.coordinates,
                "gravity": data.surfacecourse.gravity,
            }
        elif data.course_type == Course.COURSE_SRVRALLY:
            prepped['course_info'] = {
                "vehicle_type": data.srvrallycourse.vehicle_type,
                "planet_name": data.srvrallycourse.planet_name,
                "length": data.srvrallycourse.length,
                "start_port_name": data.srvrallycourse.start_port_name,
                "end_port_name": data.srvrallycourse.end_port_name,
                "starting_line": data.srvrallycourse.starting_line,
                "finish_line": data.srvrallycourse.finish_line,
                "gravity": data.srvrallycourse.gravity,
                "planet_type": data.srvrallycourse.planet_type,
            }
        elif data.course_type == Course.COURSE_SRVCROSS:
            prepped['course_info'] = {
                "vehicle_type": data.srvcrosscourse.vehicle_type,
                "planet_name": data.srvcrosscourse.planet_name,
                "port_name": data.srvcrosscourse.port_name,
                "gravity": data.srvcrosscourse.gravity,
                "tidally_locked": data.srvcrosscourse.tidally_locked,
            }
        elif data.course_type == Course.COURSE_STADIUM:
            prepped['course_info'] = {
                "vehicle_type": data.stadiumcourse.vehicle_type,
                "planet_name": data.stadiumcourse.planet_name,
                "port_name": data.stadiumcourse.port_name,
                "gravity": data.stadiumcourse.gravity,
            }

        return prepped

    def random_course(self):
        # Order by random, then take the first one.
        random_order = self.base_qs.order_by('?')

        if random_order.exists():
            return random_order[0]

        raise NotFound('No courses found.')

    @classmethod
    def urls(cls, name_prefix=None):
        urlpatterns = super(CourseResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + [
            url(
                r'^random/$',
                cls.as_view('random_course'),
                name=cls.build_url_name('random_course', name_prefix)
            ),
        ]
