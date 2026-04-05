from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Line

# @admin.register(Route)
# class RouteAdmin(gis_admin.GISModelAdmin):
#     list_display = ['name']

# @admin.register(RouteRun)
# class RouteRunAdmin(admin.ModelAdmin):
#     list_display = ['route', 'started_at', 'direction']
#     list_filter = ['direction', 'route']
#     date_hierarchy = 'started_at'

@admin.register(Line)
class LineAdmin(gis_admin.GISModelAdmin):
    list_display = ['pk','name']

# @admin.register(Trail)
# class TrailAdmin(gis_admin.GISModelAdmin):
#     list_display = ['name']