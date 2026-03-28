from django.urls import path
from .views import IngestActivitiesView

urlpatterns = [
    path('activities/', IngestActivitiesView.as_view(), name='ingest-activities'),
]