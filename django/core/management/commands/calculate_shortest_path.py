from django.core.management.base import BaseCommand
from neomodel import db as neo_db


DELETE_QUERY="""
MATCH ()-[r:TRAVELS_TO]->()
DELETE r
"""


BUILD_QUERY="""
MATCH (a:Junction)<-[:STARTS_AT]-(s:Segment)-[:ENDS_AT]->(b:Junction)

MERGE (a)-[:TRAVELS_TO {
    distance_meters: s.distance_meters,
    segment_id: s.unique_id
}]->(b)

MERGE (b)-[:TRAVELS_TO {
    distance_meters: s.distance_meters,
    segment_id: s.unique_id
}]->(a)
"""


DROP_PROJECTION_QUERY = """
CALL gds.graph.drop('junction_graph', false)
"""


PROJECT_QUERY = """
CALL gds.graph.project(
    'junction_graph',
    'Junction',
    {
        TRAVELS_TO: {
            properties: 'distance_meters'
        }
    }
)
"""


SUM_QUERY="""
MATCH (start:Junction {unique_id: $start_id}),
      (end:Junction {unique_id: $end_id})

CALL gds.shortestPath.dijkstra.stream('junction_graph', {
    sourceNode: start,
    targetNode: end,
    relationshipWeightProperty: 'distance_meters'
})
YIELD totalCost, nodeIds, path

RETURN
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).unique_id] AS pat
"""


class Command(BaseCommand):
    help = 'Project junction graph and calculate shortest path between two junctions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start-id',
            type=str,
            required=True,
            help='Unique ID of the start junction',
        )
        parser.add_argument(
            '--end-id',
            type=str,
            required=True,
            help='Unique ID of the end junction',
        )
        parser.add_argument(
            '--build',
            action='store_true',
            help='Build TRAVELS_TO relationships and project graph before calculating path',
        )
        parser.add_argument(
            '--rebuild',
            action='store_true',
            help='Delete existing TRAVELS_TO relationships before rebuilding',
        )

    def handle(self, *args, **options):
        start_id = options['start_id']
        end_id = options['end_id']

        if options['rebuild']:
            self.stdout.write('Clearing existing TRAVELS_TO rels...')
            neo_db.cypher_query(DELETE_QUERY)
        if options['build'] or options['rebuild']:
            self.stdout.write('Creating new TRAVELS_TO rels...')
            neo_db.cypher_query(BUILD_QUERY)
        self.stdout.write(self.style.SUCCESS('TRAVELS_TO relationships created'))

        self.stdout.write('Projecting in-memory graph...')
        neo_db.cypher_query(DROP_PROJECTION_QUERY)
        neo_db.cypher_query(PROJECT_QUERY)

        self.stdout.write('Calculating shortest path...')
        try:
            results, _ = neo_db.cypher_query(SUM_QUERY, {'start_id': start_id, 'end_id': end_id})
            if results:
                total_cost, path = results[0]
                self.stdout.write(f'Total distance: {total_cost:.0f} meters')
                self.stdout.write(f'Path: {" -> ".join(path)}')
            else:
                self.stdout.write('No path found between the given junctions.')
        finally:
            self.stdout.write('Dropping in-memory graph projection...')
            neo_db.cypher_query(DROP_PROJECTION_QUERY)