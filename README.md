```
docker compose build
```

```
docker compose up -d
```

```
docker compose exec django python manage.py makemigrations
```

```
docker compose exec django python manage.py migrate
```

```
docker compose exec django python manage.py migrate --database=geospatial
```

---

```
docker compose exec django python manage.py shell
```

```python
from postgis_app.models import TrailSegment, Route
from django.contrib.gis.geos import LineString, MultiLineString

sample_line = LineString(
    ( -110.852, 32.233 ), 
    ( -110.850, 32.234 ), 
    ( -110.848, 32.236 )
)

trail_segment = TrailSegment.objects.create(
    name='Sample Trail Segment',
    geometry=sample_line
)

route = Route.objects.create(
    name='Sample Route',
    geometry=MultiLineString(sample_line)
)
```