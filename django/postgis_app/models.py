from django.contrib.gis.db import models


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