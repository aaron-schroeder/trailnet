import json

from django.contrib.gis.geos import LineString
from django.core.management.base import BaseCommand, CommandError

from postgis_app.models import Line


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            type=str,
            help='Path of geojson file',
        )

    def handle(self, *args, **options):
        file_path = options['path']
        try:
            with open(file_path, 'r') as f:
                featurecollection = json.load(f)
        except FileNotFoundError:
            raise CommandError(f'File not found: {file_path}')
        except json.JSONDecodeError:
            raise CommandError(f'Invalid JSON in file: {file_path}')
        features = featurecollection.get('features')
        if not features:
            raise CommandError('GeoJSON does not contain "features"')
        created_count = 0
        skipped_count = 0
        for feature in featurecollection['features']:
            properties = feature.get('properties', {})
            name = properties.get('name')
            geometry = feature.get('geometry', {})
            geometry_type = geometry.get('type')
            self.stdout.write(
                f'Feature {properties.get("id", "—")}: '
                f'name="{name or "Unnamed"}", '
                f'geometry.type={geometry_type}'
            )
            if geometry_type == 'LineString':
                coords = geometry.get('coordinates')
                if not coords:
                    skipped_count += 1
                    continue
                try:
                    linestring = LineString([tuple(coord) for coord in coords])
                except Exception as e:
                    self.stderr.write(f'Invalid coordinates: {e}')
                    skipped_count += 1
                    continue

                # Line.objects.create(
                #     name=name,
                #     geometry=linestring
                # )
                # created_count += 1

                # Check geometry uniqueness to avoid creating a duplicate identical Line
                if not Line.objects.filter(geometry__equals=linestring).exists():
                    Line.objects.create(
                        name=name,
                        geometry=linestring
                    )
                    created_count += 1
                else:
                    skipped_count += 1

            else:
                skipped_count += 1
        self.stdout.write(
            self.style.SUCCESS(
                    f'Created {created_count} Lines '
                    f'(skipped {skipped_count})'
                )
        )