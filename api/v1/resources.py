import time

from restless.exceptions import BadRequest
from restless.dj import DjangoResource

from courses.models import Course


class CourseResource(DjangoResource):
    def list(self):
        try:
            start = int(self.request.GET.get('start', 0)) or None
            limit = int(self.request.GET.get('limit', 100))
        except ValueError:
            raise BadRequest("Invalid start/limit parameters.")

        if limit > 1000:
            limit == 1000

        if start is not None:
            return Course.objects.filter(pk__lte=start)[:limit]

        return Course.objects.all()[:limit]

    def detail(self, pk):
        return Course.objects.get(id=pk)

    def wrap_list_response(self, data):
        # FIXME: Add pagination URLs here.
        return {
            'meta': {
                'start': int(self.request.GET.get('start', 0)) or None,
                'limit': int(self.request.GET.get('limit', 100)),
                'total': Course.objects.all().count(),
            },
            'courses': data,
        }

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
            "created": time.mktime(data.created.timetuple()) * 1000,
            "url": data.get_absolute_url(),
        }

        for screenshot in data.screenshots.all():
            # FIXME: Verify this.
            prepped['screenshots'].append(screenshot.url)

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