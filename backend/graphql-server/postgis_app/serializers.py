from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import TrailSegment

class TrailSegmentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = TrailSegment
        fields = ('id', 'name', 'geometry')  # Specify fields explicitly
        geo_field = 'geometry'  # This field will be serialized as GeoJSON