from django.contrib import admin

from .models import (
    Course,
    ZeroGravityCourse,
    SurfaceCourse,
    SRVRallyCourse,
    SRVCrossCourse,
    StadiumCourse,
    CourseScreenshot,
)


class ZeroGravityCourseInline(admin.StackedInline):
    model = ZeroGravityCourse
    exclude = ('vehicle_type', 'created', 'updated')


class SurfaceCourseInline(admin.StackedInline):
    model = SurfaceCourse
    exclude = ('vehicle_type', 'created', 'updated')


class SRVRallyCourseInline(admin.StackedInline):
    model = SRVRallyCourse
    exclude = ('vehicle_type', 'created', 'updated')


class SRVCrossCourseInline(admin.StackedInline):
    model = SRVCrossCourse
    exclude = ('vehicle_type', 'created', 'updated')


class StadiumCourseInline(admin.StackedInline):
    model = StadiumCourse
    exclude = ('vehicle_type', 'created', 'updated')


class CourseScreenshotInline(admin.StackedInline):
    model = CourseScreenshot
    extra = 0
    exclude = ('created', 'updated')


class CourseAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    inlines = [
        ZeroGravityCourseInline,
        SurfaceCourseInline,
        SRVRallyCourseInline,
        SRVCrossCourseInline,
        StadiumCourseInline,
        CourseScreenshotInline,
    ]
    list_display = ('title', 'system', 'course_type', 'created_by', 'created')
    list_filter = ('course_type',)
    search_fields = ('title', 'system', 'notes', 'created_by__name')
    raw_id_fields = ('created_by',)


class CourseScreenshotAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('course', 'shot', 'is_primary', 'created')
    list_filters = ('is_primary', 'is_annotated')
    search_fields = ('course__title',)
    raw_id_fields = ('course',)


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseScreenshot, CourseScreenshotAdmin)
