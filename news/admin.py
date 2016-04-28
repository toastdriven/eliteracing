from django.contrib import admin

from .models import NewsPost


class NewsPostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    exclude = ('content_html',)
    list_display = ('title', 'author', 'created')
    prepopulated_fields = {
        "slug": ("title",)
    }
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)


admin.site.register(NewsPost, NewsPostAdmin)
