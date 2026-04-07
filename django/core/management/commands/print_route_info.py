from postgis_app.models.graph import Route

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        route = Route.nodes.get(unique_id='route_1')

        ordered = sorted(
            route.steps.all(),
            key=lambda rs: rs.order
        )
        for rs in ordered:
            seg = rs.segment.single()
            print(f"{rs.order}: {seg.unique_id} ({rs.direction})")
