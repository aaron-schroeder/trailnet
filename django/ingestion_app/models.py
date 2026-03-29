from django.contrib.gis.db import models
from django.db import models as base_models


class Activity(models.Model):
    source = base_models.CharField(max_length=50)
    external_id = base_models.CharField(max_length=100, unique=True)
    started_at = base_models.DateTimeField()
    geometry = models.LineStringField()          # derived summary, for spatial queries
    raw = base_models.JSONField()                # full original payload, preserved
    ingested_at = base_models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self):
        return f"{self.source}:{self.external_id} @ {self.started_at}"

    class AlreadyExists(Exception):
        pass

# class ActivityPoint(models.Model):
#     activity = base_models.ForeignKey(
#         Activity,
#         on_delete=base_models.CASCADE,
#         related_name='points'
#     )
#     sequence = base_models.PositiveIntegerField()
#     timestamp = base_models.DateTimeField()
#     location = models.PointField()               # lon, lat
#     elevation = base_models.FloatField(null=True)

#     class Meta:
#         ordering = ['sequence']
#         indexes = [
#             base_models.Index(fields=['activity', 'sequence']),
#         ]

#     def __str__(self):
#         return f"{self.activity.external_id}[{self.sequence}] @ {self.timestamp}"