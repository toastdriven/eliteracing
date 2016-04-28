from django.contrib import admin

from .models import Page


class PageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    exclude = ('content_html',)
    list_display = ('title', 'created')
    prepopulated_fields = {
        "slug": ("title",)
    }
    search_fields = ('title', 'content')


admin.site.register(Page, PageAdmin)
