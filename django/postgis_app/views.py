from rest_framework import viewsets
from .models import TrailSegment
from .serializers import TrailSegmentSerializer

class TrailSegmentViewSet(viewsets.ModelViewSet):
    queryset = TrailSegment.objects.all()
    serializer_class = TrailSegmentSerializer
