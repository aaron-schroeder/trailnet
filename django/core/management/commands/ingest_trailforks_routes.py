import json

from django.contrib.gis.geos import MultiLineString, LineString
from django.core.management.base import BaseCommand, CommandError
import polyline

from postgis_app.models import Route


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('/app/scripts/rms.json', 'r') as f:
            featurecollection = json.load(f)
        created_count = 0
        skipped_count = 0
        for feature in featurecollection['features']:
            properties = feature.get('properties')
            name = properties.get('name')
            trailforks_type = properties.get('type')
            geometry = feature.get('geometry')
            geometry_type = geometry.get('type')
            self.stdout.write(
                f'Feature {properties.get("id", "—")}: '
                f'name="{name or "Unnamed"}", '
                f'trailforks_type={trailforks_type}, '
                f'geometry.type={geometry_type}'
            )
            if trailforks_type == 'trail':
                try:
                    coordinates = polyline.decode(geometry.get('encodedpath'))
                except IndexError:
                    print(f'Something odd about {name}')
                    print(geometry.get('encodedpath'))
                Route.objects.create(
                    name=name,
                    geometry=MultiLineString(LineString([(c[1], c[0]) for c in coordinates]))
                )
                created_count += 1
            else:
                skipped_count += 1
        self.stdout.write(
            self.style.SUCCESS(
                    f'Created {created_count} Routes '
                    f'(skipped {skipped_count})'
                )
        )