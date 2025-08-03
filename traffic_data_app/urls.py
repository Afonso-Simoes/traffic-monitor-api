from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoadSegmentViewSet, TrafficReadingViewSet

router = DefaultRouter()
router.register("roadsegments", RoadSegmentViewSet, basename="roadsegment")
router.register("trafficreadings", TrafficReadingViewSet, basename="trafficreading")

urlpatterns = [
    path("", include(router.urls)),
]
