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
    max_num = 1


class SurfaceCourseInline(admin.StackedInline):
    model = SurfaceCourse
    max_num = 1


class SRVRallyCourseInline(admin.StackedInline):
    model = SRVRallyCourse
    max_num = 1


class SRVCrossCourseInline(admin.StackedInline):
    model = SRVCrossCourse
    max_num = 1


class StadiumCourseInline(admin.StackedInline):
    model = ZeroGravityCourse
    max_num = 1


class CourseScreenshotInline(admin.StackedInline):
    model = CourseScreenshot


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
    list_filters = ('course_type',)
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
