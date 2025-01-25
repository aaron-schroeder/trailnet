from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrailSegmentViewSet, TrailViewSet, RouteViewSet

router = DefaultRouter()
router.register(r'trail-segments', TrailSegmentViewSet)
router.register(r'trails', TrailViewSet)
router.register(r'routes', RouteViewSet)


urlpatterns = [
    path('', include(router.urls)),
]