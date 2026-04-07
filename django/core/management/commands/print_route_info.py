from postgis_app.models.graph import Route

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        route = Route.nodes.get(unique_id='route_1')

        segments = route.segments.all()
        # for seg in segments:
        #     print(seg.unique_id, seg.name, seg.distance_meters)

        # v1:
        ordered_segments = sorted(
            [(seg, route.segments.relationship(seg)) for seg in segments],
            key=lambda x: x[1].order
        )
        for seg, rel in ordered_segments:
            print(f"{rel.order}: {seg.unique_id} ({rel.direction}) - {seg.distance_meters} meters")

        # v2:
        ordered = sorted(
            route.steps.all(),
            key=lambda rs: rs.order
        )
        for rs in ordered:
            seg = rs.segment.single()
            print(f"{rs.order}: {seg.unique_id} ({rs.direction})")
