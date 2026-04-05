from django.contrib.gis.db import models
from django.db import models as base_models


class Line(models.Model):
    name = models.CharField(max_length=100)
    # source = models.CharField(max_length=100, blank=True)  # NEW e.g. 'trailforks', 'strava', 'manual'
    geometry = models.LineStringField()

    def __str__(self):
        return self.name

# class Trail(models.Model):
#     name = models.CharField(max_length=100)
#     geometry = models.MultiLineStringField()

#     def __str__(self):
#         return self.name


# class Route(models.Model):
#     name = models.CharField(max_length=100)
#     # segments = models.ManyToManyField(TrailSegment)
#     geometry = models.MultiLineStringField() 

#     def __str__(self):
#         return self.name


# class Direction(base_models.TextChoices):
#     FORWARD = 'F', 'Forward'
#     REVERSE = 'R', 'Reverse'


# # class TrailSegmentRun(models.Model):
# #     """Roughly equivalent to `strava.SegmentEffort`"""
# #     trail_segment = models.ForeignKey(TrailSegment, on_delete=models.CASCADE, related_name='runs')
# #     started_at = models.DateTimeField()
# #     direction = models.CharField(max_length=1, choices=Direction.choices)


# class RouteRun(models.Model):
#     """Roughly equivalent to Strava's concept of a 'matched run'"""
#     route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='runs')
#     started_at = models.DateTimeField()
#     direction = models.CharField(max_length=1, choices=Direction.choices)