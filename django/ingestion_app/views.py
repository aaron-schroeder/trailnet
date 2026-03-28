import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.gis.geos import LineString, Point
from django.utils.dateparse import parse_datetime
from django.db import transaction
from .models import Activity, ActivityPoint


def require_token(fn):
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization', '').removeprefix('Token ').strip()
        from django.conf import settings
        if token != settings.INGESTION_API_TOKEN:
            return JsonResponse({'error': 'unauthorized'}, status=401)
        return fn(request, *args, **kwargs)
    return wrapper


@method_decorator([csrf_exempt, require_token], name='dispatch')
class IngestActivitiesView(View):

    def post(self, request):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'invalid json'}, status=400)

        activities = body.get('activities', [])
        if not activities:
            return JsonResponse({'error': 'no activities provided'}, status=400)

        created, skipped, errors = [], [], []

        for raw in activities:
            try:
                self._ingest_one(raw)
                created.append(raw['external_id'])
            except Activity.AlreadyExists:
                skipped.append(raw['external_id'])
            except Exception as e:
                errors.append({'external_id': raw.get('external_id'), 'error': str(e)})

        return JsonResponse({
            'created': len(created),
            'skipped': len(skipped),
            'errors': errors,
        }, status=207)

    @transaction.atomic
    def _ingest_one(self, raw):
        if Activity.objects.filter(source=raw['source'], external_id=raw['external_id']).exists():
            raise Activity.AlreadyExists()

        coords = raw['coordinates']  # each: [lon, lat, elevation_or_null, iso_timestamp]

        geometry = LineString([(c[0], c[1]) for c in coords])

        activity = Activity.objects.create(
            source=raw['source'],
            external_id=raw['external_id'],
            started_at=raw['started_at'],
            geometry=geometry,
            raw=raw,
        )

        ActivityPoint.objects.bulk_create([
            ActivityPoint(
                activity=activity,
                sequence=i,
                timestamp=parse_datetime(c[3]),
                location=Point(c[0], c[1]),
                elevation=c[2] if c[2] is not None else None,
            )
            for i, c in enumerate(coords)
        ])