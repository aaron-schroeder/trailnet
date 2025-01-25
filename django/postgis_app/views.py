from rest_framework import viewsets
from .models import TrailSegment, Trail, Route
from .serializers import TrailSegmentSerializer, TrailSerializer, RouteSerializer


class TrailSegmentViewSet(viewsets.ModelViewSet):
    queryset = TrailSegment.objects.all()
    serializer_class = TrailSegmentSerializer


class TrailViewSet(viewsets.ModelViewSet):
    queryset = Trail.objects.all()
    serializer_class = TrailSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer