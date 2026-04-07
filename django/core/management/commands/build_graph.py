from django.core.management.base import BaseCommand
from django.db import connection
from neomodel import db as neo_db
from postgis_app.models.postgis import Line
from postgis_app.models.graph import Junction, Segment


TOLERANCE_METERS = 3


CLUSTER_SQL = """
WITH endpoints AS (
    SELECT
        id AS line_id,
        name AS line_name,
        'start' AS end_type,
        ST_StartPoint(geometry) AS point
    FROM postgis_app_line

    UNION ALL

    SELECT
        id AS line_id,
        name AS line_name,
        'end' AS end_type,
        ST_EndPoint(geometry) AS point
    FROM postgis_app_line
),
clusters AS (
    SELECT
        unnest(ST_ClusterWithin(point, %(tolerance)s)) AS geom
    FROM endpoints
),
clustered_points AS (
    SELECT
        row_number() OVER () AS cluster_id,
        (ST_Dump(geom)).geom AS point
    FROM clusters
)
SELECT
    e.line_id,
    e.line_name,
    e.end_type,
    ST_X(e.point) AS lon,
    ST_Y(e.point) AS lat,
    cp.cluster_id
FROM endpoints e
JOIN clustered_points cp
    ON ST_DWithin(e.point, cp.point, %(tolerance)s)
ORDER BY e.line_id, e.end_type;
"""


class Command(BaseCommand):
    help = 'Build Neo4j graph (Junctions and Segments) from PostGIS Line geometry'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tolerance',
            type=float,
            default=TOLERANCE_METERS,
            help='Junction clustering tolerance in meters '
                 f'(default: {TOLERANCE_METERS:.0f})',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing Junction and Segment nodes before rebuilding',
        )

    def handle(self, *args, **options):
        tolerance = options['tolerance']
        tolerance_degrees = tolerance / 111_000  # rough conversion, good enough

        if options['clear']:
            self.stdout.write('Clearing existing graph...')
            neo_db.cypher_query('MATCH (n:Segment) DETACH DELETE n')
            neo_db.cypher_query('MATCH (n:Junction) DETACH DELETE n')
            self.stdout.write('Cleared.')

        self.stdout.write('Clustering endpoints...')
        endpoint_rows = self._cluster_endpoints(tolerance_degrees)

        # endpoint_rows: list of (line_id, end_type, lon, lat, cluster_id)
        # Build lookup: cluster_id -> Junction node
        self.stdout.write('Creating Junction nodes...')
        cluster_to_junction = self._create_junctions(endpoint_rows)

        self.stdout.write('Creating Segment nodes...')
        self._create_segments(endpoint_rows, cluster_to_junction)

        self.stdout.write(self.style.SUCCESS(
            f'Done. {len(cluster_to_junction)} junctions, '
            f'{Line.objects.count()} segments.'
        ))

    def _cluster_endpoints(self, tolerance_degrees):
        with connection.cursor() as cursor:
            cursor.execute(CLUSTER_SQL, {'tolerance': tolerance_degrees})
            return cursor.fetchall()

    def _create_junctions(self, rows):
        seen_clusters = {}
        for line_id, line_name, end_type, lon, lat, cluster_id in rows:
            if cluster_id not in seen_clusters:
                junction = Junction(
                    unique_id=f'junction_{cluster_id}',
                ).save()
                seen_clusters[cluster_id] = junction
        return seen_clusters

    def _create_segments(self, rows, cluster_to_junction):
        # reorganize rows by line_id
        by_line = {}
        for line_id, line_name, end_type, lon, lat, cluster_id in rows:
            if line_id not in by_line:
                by_line[line_id] = {'name': line_name}
            by_line[line_id][end_type] = cluster_id

        for line_id, ends in by_line.items():
            start_cluster = ends.get('start')
            end_cluster = ends.get('end')

            if start_cluster is None or end_cluster is None:
                self.stdout.write(
                    self.style.WARNING(f'Line {line_id} missing an endpoint cluster, skipping.')
                )
                continue

            segment = Segment(
                unique_id=f'segment_{line_id}',
                name = ends.get('name'),
                line_id=line_id,
            ).save()

            segment.start_junction.connect(cluster_to_junction[start_cluster])
            segment.end_junction.connect(cluster_to_junction[end_cluster])