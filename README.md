```
docker-compose build
```

```
docker-compose run
```

```
docker-compose exec django python manage.py makemigrations
```

```
docker-compose exec django python manage.py migrate
```

```
docker-compose exec django python manage.py migrate --database=geospatial
```

---

```
docker-compose exec django python manage.py shell
```

```
>>> from postgis_app.models import TrailSegment
>>> from django.contrib.gis.geos import LineString
>>> sample_line = LineString(( -110.852, 32.233 ), ( -110.850, 32.234 ), ( -110.848, 32.236 ))
>>> trail_segment = TrailSegment(name="Sample Trail Segment", geometry=sample_line)
>>> trail_segment.save()
>>> exit()
```