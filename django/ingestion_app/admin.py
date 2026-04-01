from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(gis_admin.GISModelAdmin):
    list_display = ['source', 'external_id']


# BAD IDEA to keep so many datapoints as Django ORM objects.
# Prohibitively slow.
# Re-evaluating intent currently.
# @admin.register(ActivityPoint)
# class ActivityPointAdmin(gis_admin.GISModelAdmin):
#     list_display = ['activity', 'sequence']