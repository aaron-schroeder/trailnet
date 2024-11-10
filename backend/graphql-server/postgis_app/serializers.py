from rest_framework import serializers
from .models import TrailSegment

class TrailSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrailSegment
        fields = '__all__'