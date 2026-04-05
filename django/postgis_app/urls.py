from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LineViewSet

router = DefaultRouter()
router.register(r'lines', LineViewSet)


urlpatterns = [
    path('', include(router.urls)),
]