# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from poi.views import PointOfInterestViewSet

router = DefaultRouter()
router.register(r'pois', PointOfInterestViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
