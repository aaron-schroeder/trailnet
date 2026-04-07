from django.core.management.base import BaseCommand
from django.db import connection
from neomodel import db as neo_db

from postgis_app.models.graph import Route, Segment, RouteStep, Junction


class Command(BaseCommand):
    help = "Build a pre-set Route consisting of some existing Segments"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing Route nodes before rebuilding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing Routes...')
            neo_db.cypher_query('MATCH (n:Route) DETACH DELETE n')
        line_id_list = [2751, 2755, 2756, 2713, 2712, 2752, 2753, 2754, 2751]
        segment_list = [
            Segment.nodes.get(unique_id=f'segment_{lid:.0f}')
            for lid in line_id_list
        ]
        route = build_route(
            'route_1',
            'Test Route',
            segment_list,
            first_segment_direction='F',
        )


def build_route(route_id: str, name: str, segment_sequence: list[Segment], first_segment_direction='F'):
    route = Route(unique_id=route_id, name=name).save()
    prev_end = None
    for order, segment in enumerate(segment_sequence):
        if order == 0:
            # Specify the direction of the first Segment traversal
            direction = first_segment_direction
            start, end = get_junctions(segment, direction)
        else:
            direction, end = infer_direction(prev_end, segment)
            start, _ = get_junctions(segment, direction)
            if prev_end and start.unique_id != prev_end.unique_id:
                raise ValueError(
                    f'Segment {segment.unique_id} does not connect to previous segment'
                )

        print({
            'id': segment.unique_id,
            'order': order,
            'direction': direction
        })

        # v1: Connect the Segment to the Route
        route.segments.connect(
            segment,
            {
                'order': order,
                'direction': direction
            }
        )

        # v2: Create and connect the RouteStep node
        step = RouteStep(
            order=order,
            direction=direction
        ).save()
        route.steps.connect(step)
        step.segment.connect(segment)

        prev_end = end
    return route


def get_junctions(segment: Segment, direction: str):
    start = list(segment.start_junction)[0]
    end = list(segment.end_junction)[0]

    if direction == 'F':
        return start, end
    elif direction == 'R':
        return end, start
    else:
        raise ValueError(f"Invalid direction: {direction}")
    

def infer_direction(prev_junction: Junction, segment: Segment):
    start = list(segment.start_junction)[0]
    end = list(segment.end_junction)[0]

    if prev_junction.unique_id == start.unique_id:
        return 'F', end
    elif prev_junction.unique_id == end.unique_id:
        return 'R', start
    else:
        raise ValueError("Segment does not connect")