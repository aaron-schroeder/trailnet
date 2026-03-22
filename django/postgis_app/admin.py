from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import TrailSegment, Trail, Route

# Register your models here.
@admin.register(Route)
class RouteAdmin(gis_admin.GISModelAdmin):
    list_display = ['name']

@admin.register(TrailSegment)
class TrailSegmentAdmin(gis_admin.GISModelAdmin):
    list_display = ['name']

@admin.register(Trail)
class TrailAdmin(gis_admin.GISModelAdmin):
    list_display = ['name']