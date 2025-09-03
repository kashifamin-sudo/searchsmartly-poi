# serializers.py
from rest_framework import serializers
from .models import PointOfInterest

class PointOfInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfInterest
        fields = [
            'id', 'external_id', 'name', 'latitude', 'longitude',
            'category', 'average_rating', 'description'
        ]
