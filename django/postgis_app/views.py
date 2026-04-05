from django.http import JsonResponse
from rest_framework import viewsets

from .models import Line, Segment
from .serializers import LineSerializer


class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer


def graph_json(request):
    """Return data for all Segments
        - Segment ID
        - Segment line_id (pk for `Line` object)
        - Segment Name
        - Start Junction ID
        - End Junction ID
        - Start coordinate (Dict['lon','lat'])
        - End coordinate (Dict['lon','lat'])
    """
    results = []

    for segment in Segment.nodes.all():
        start_junction = segment.start_junction.single()
        end_junction = segment.end_junction.single()

        try:
            line = Line.objects.get(pk=segment.line_id)
        except Line.DoesNotExist:
            continue

        coords = line.geometry.coords  # list of (lon, lat) tuples
        start_coord = coords[0]
        end_coord = coords[-1]

        results.append({
            'unique_id': segment.unique_id,
            'line_id': segment.line_id,
            'name': segment.name,
            'start_junction': start_junction.unique_id if start_junction else None,
            'end_junction': end_junction.unique_id if end_junction else None,
            'start_coord': {'lon': start_coord[0], 'lat': start_coord[1]},
            'end_coord': {'lon': end_coord[0], 'lat': end_coord[1]},
        })

    return JsonResponse({'segments': results})