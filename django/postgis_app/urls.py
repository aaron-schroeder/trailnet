from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrailSegmentViewSet

router = DefaultRouter()
router.register(r'trail-segments', TrailSegmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]