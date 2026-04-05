from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Line


class LineSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Line
        fields = ('id', 'name', 'geometry')
        geo_field = 'geometry'
