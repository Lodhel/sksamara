#coding=utf8
from django.contrib import admin
from sksamara.models import StaticPage, ConnectionRequest, ConnectionRequestFile, SiteSettings


class StaticPageAdmin(admin.ModelAdmin):
    list_display = 'title', 'slug', 'publish', 'order'
    list_editable = 'publish', 'order'
    save_on_top = True

    class Media:
        js = '/static/js/jquery.synctranslit.js', '/static/js/admin.js'

admin.site.register(StaticPage, StaticPageAdmin)


class ConnectionRequestFileInline(admin.TabularInline):
    model = ConnectionRequestFile
    extra = 0


class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = 'date', 'full_name', 'email', 'status', 'city'
    list_filter = 'date', 'status'
    inlines = ConnectionRequestFileInline,

admin.site.register(ConnectionRequest, ConnectionRequestAdmin)


class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return SiteSettings.objects.count() == 0

admin.site.register(SiteSettings, SiteSettingsAdmin)


