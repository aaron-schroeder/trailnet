from django.contrib.gis.db import models
from django.db import models as base_models


class TrailSegment(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.LineStringField()

    def __str__(self):
        return self.name


class Trail(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.MultiLineStringField()

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=100)
    # segments = models.ManyToManyField(TrailSegment)
    geometry = models.MultiLineStringField() 

    def __str__(self):
        return self.name


class Direction(base_models.TextChoices):
    FORWARD = 'F', 'Forward'
    REVERSE = 'R', 'Reverse'


class RouteRun(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='runs')
    started_at = models.DateTimeField()
    direction = models.CharField(max_length=1, choices=Direction.choices)