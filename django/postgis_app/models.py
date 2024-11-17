from django.contrib.gis.db import models


class TrailSegment(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.LineStringField()