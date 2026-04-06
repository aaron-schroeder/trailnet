from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    FloatProperty,
    RelationshipTo,
    RelationshipFrom,
    StructuredRel,
)


class Junction(StructuredNode):
    unique_id = StringProperty(unique_index=True)


class SegmentEndRel(StructuredRel):
    """Carries no properties for now, but named so the relationship
    itself is queryable and extensible later."""
    pass


class Segment(StructuredNode):
    unique_id = StringProperty(unique_index=True, required=True)
    line_id = IntegerProperty()  # FK into PostGIS Line.pk
    name = StringProperty()
    distance_meters = FloatProperty()


    start_junction = RelationshipTo(Junction, 'STARTS_AT', model=SegmentEndRel)
    end_junction = RelationshipTo(Junction, 'ENDS_AT', model=SegmentEndRel)

    def __str__(self):
        return self.name


class RouteSegmentRel(StructuredRel):
    order = IntegerProperty(required=True)
    direction = StringProperty(required=True)  # 'F' or 'R'


class Route(StructuredNode):
    unique_id = StringProperty(unique_index=True, required=True)
    name = StringProperty()

    segments = RelationshipTo(Segment, 'INCLUDES', model=RouteSegmentRel)

    def __str__(self):
        return self.name


# BELOW THIS POINT - STUFF TO ADD LATER

# class Direction(base_models.TextChoices):
#     FORWARD = 'F', 'Forward'
#     REVERSE = 'R', 'Reverse'


# class TrailSegmentRun(models.Model):
#     """Roughly equivalent to `strava.SegmentEffort`"""
#     trail_segment = models.ForeignKey(TrailSegment, on_delete=models.CASCADE, related_name='runs')
#     started_at = models.DateTimeField()
#     direction = models.CharField(max_length=1, choices=Direction.choices)


# class RouteRun(models.Model):
#     """Roughly equivalent to Strava's concept of a 'matched run'"""
#     route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='runs')
#     started_at = models.DateTimeField()
#     direction = models.CharField(max_length=1, choices=Direction.choices)


# class Trail(models.Model):
#     name = models.CharField(max_length=100)
#     geometry = models.MultiLineStringField()

#     def __str__(self):
#         return self.name