from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import TrailSegment, Trail, Route


class TrailSegmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrailSegment
        fields = ('id', 'name', 'geometry')
        geo_field = 'geometry'


class TrailSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Trail
        fields = ('id', 'name', 'geometry')  
        geo_field = 'geometry'


class RouteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'name', 'geometry')  
        geo_field = 'geometry'