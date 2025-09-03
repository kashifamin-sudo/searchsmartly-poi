# views.py
from rest_framework import viewsets, filters
from .models import PointOfInterest
from .serializers import PointOfInterestSerializer

class PointOfInterestViewSet(viewsets.ModelViewSet):
    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'external_id', 'name']
    ordering_fields = ['average_rating', 'created_at']
