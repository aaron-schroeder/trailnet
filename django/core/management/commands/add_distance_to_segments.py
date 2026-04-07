from django.core.management.base import BaseCommand
from django.db import connection
from postgis_app.models.graph import Segment


class Command(BaseCommand):
    help = "Populate Segment.distance from PostGIS Line geometry"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, ST_Length(geometry::geography) AS distance
                FROM postgis_app_line
            """)
            rows = cursor.fetchall()

        # Build lookup: {line_id: distance}
        line_distances = {row[0]: row[1] for row in rows}

        updated = 0
        missing = 0
        for seg in Segment.nodes:
            dist = line_distances.get(seg.line_id)
            if dist is None:
                missing += 1
                continue
            seg.distance_meters = round(dist, 1)
            seg.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Updated {updated} segments, {missing} missing line refs'
        ))
