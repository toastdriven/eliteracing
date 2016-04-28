from django.contrib import admin

from .models import Commander


class CommanderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name', 'user', 'api_token', 'created')
    search_fields = ('name',)
    raw_id_fields = ('user',)


admin.site.register(Commander, CommanderAdmin)
