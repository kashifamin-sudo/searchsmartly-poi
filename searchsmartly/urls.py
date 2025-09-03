from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from poi.views import PointOfInterestViewSet

# Register DRF viewsets
router = DefaultRouter()
router.register(r'pois', PointOfInterestViewSet, basename='poi')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include(router.urls)),

    # Optional: DRF's browsable API auth
    path('api-auth/', include('rest_framework.urls')),
]
