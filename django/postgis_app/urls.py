from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LineViewSet, graph_json

router = DefaultRouter()
router.register(r'lines', LineViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('graph/', graph_json, name='graph-json'),
]