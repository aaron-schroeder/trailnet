## quickstart - example flow
1. (Optional) Clean slate - [delete objects](#delete-all-objects-of-one-model-class)
2. Load model objects
    - Load `Line` objects into the PostGIS db from the processed .geojson file 
      (made elsewhere using QGIS to work with the raw TrailForks data)
      ([see howto](#load-line-objects-from-canonical-segments))
    - Create the graph of the trail network (`Segment` and `Junction`)
      by processing the collection of `Line` objects (presumed to look like a trail network)
      ([see howto](#process-collection-of-line-objects-into-a-graph-of-the-trail-network))
    - Create a manual `Route` graph object by running the `build_route` management command.
    - Add `distance_meters` property to segments by running the `add_distance_to_segments`
      management command
    - To ingest `Activity` objects into the PostGIS db, hit the POST endpoint
      (using another service) ([see howto](#ingest-activity-objects))
3. Check on the objects you've created
    - Check on your newly-created objects in Django admin ([see howto](#view-objects-in-django-admin))
    - See `Line` objects OR a combined map representing `Line`, `Segment`, and `Junction` data
      (depending on how the code is configured currently) on the React frontend app 
      ([see howto](#see-objects-on-the-react-frontend-app))
    - Print data about the manually-created `Route` by running the 
      `print_route_info` management command.
    - You can also look at the neo4j graph directly ([see howto](#see-objects-in-the-graph-database))
4. Play with the data
    - Run the `calculate_shortest_path` management command. Pre-reqs:
        - a built-up trail network consisting of a graph of `Junction` and `Segment` objects
          backed by PostGIS `Line` objects
        - A `distance_meters` property on all `Segment` objects (run `add_distance_to_segments`)


## howto

### Create objects

(Optional) You can start with a clean slate by 
[deleting all existing PostGIS objects](#delete-all-objects-of-one-model-type).

#### Load `Line` objects from canonical segments
You can load `Line` objects from the processed .geojson file
(made elsewhere using QGIS to work with the raw TrailForks data)

With the containers running, use the custom Django management command:
```sh
docker compose exec django python manage.py ingest_canonical_segments
Feature 728464: name="Pima Drop-in", geometry.type=LineString
Feature 14954: name="Pima Connector", geometry.type=LineString
# [...]
Feature 16837: name="Pima Wash Trail", geometry.type=LineString
Feature 16837: name="Pima Wash Trail", geometry.type=LineString
Created 354 Lines (skipped 0)
```

#### Load `Line` objects from TrailForks
You can also load `Line` objects from the raw TrailForks rms .json file.
Warning: This is a vestigial workflow, and it yields a crude uncurated 
`Line` network that does not behave like a network of `Segment`s and `Junction`s.
```sh
docker compose exec django python manage.py ingest_trailforks_routes
Feature 4990: name="South Mountain Preserve", trailforks_type=region, geometry.type=Point
Feature 149734: name="Parking", trailforks_type=poi, geometry.type=Point
# [...]
Feature 4990: name="South Mountain Preserve", trailforks_type=regionlabel, geometry.type=Point
Feature 1509: name="Usery Mountain Regional Park", trailforks_type=polygon, geometry.type=Polygon
Created 190 Lines (skipped 34)
```

#### Ingest `Activity` objects
Hit the POST endpoint (using another service).
For example:
```python
httpx.post(
    'http://localhost:8000/api/ingest/activities/',
    headers={'Authorization': TRAILNET_INGESTION_API_TOKEN},
    json={'activities': activities},
)
```

#### Process collection of `Line` objects into a graph of the trail network
Note: This workflow has only been tested with the nicely-curated `Line` data
from QGIS.
```sh
docker compose exec django python manage.py build_graph --clear
Clearing existing graph...
Cleared.
Clustering endpoints...
Creating Junction nodes...
Creating Segment nodes...
Done. 259 junctions, 354 segments.
```

### Delete all objects of one Model class
This currently works only for the Models managed by Django ORM (located in 
`postgis_app.models.postgis`), not for the neomodel Models in 
`postgis_app.models.graph`.

With containers running, use the custom management command.

eg. for `postgis_app.models.Line`:
```sh
docker compose exec django python manage.py delete_all_objects Line
Deleted 354 objects from postgis_app.Line
```

### View objects in Django Admin
- `Line`: http://localhost:8000/admin/postgis_app/line/
- `Activity`: http://localhost:8000/admin/ingestion_app/activity/

### See objects on the React frontend app
There's only one React endpoint currently (http://localhost:5173/) 
and I manually toggle which Map component it displays in the code.
- See geometry associated with `Segment` and `Junction` graph objects 
  (via associated `Line` object geometry) 
  (see [GraphMap.jsx](./react-app/src/components/GraphMap.jsx))
- See `Line` objects on one map 
  (see [Map.jsx](./react-app/src/components/Map.jsx))

### See objects in the graph database
neomodel / graph entities are not in django admin. 
View directly at http://localhost:7474 
(figure out username/pw using `docker-compose.yml`)

### Run a script located in django/scripts

#### From the terminal
From the terminal while the containers are running:
```sh
docker compose exec django python manage.py shell -c "exec(open('/app/scripts/${SCRIPT_NAME}.py').read())"
```

#### From the Django shell
First, follow the instructions to [enter the Django shell](#enter-the-django-shell). 
```sh
>>> exec(open('/app/scripts/${SCRIPT_NAME}.py').read())
```

### Enter the Django shell
From the terminal while the containers are running:
```
docker compose exec django python manage.py shell
```

## scratch notes
```sh
docker compose exec django python manage.py calculate_shortest_path --rebuild --start-id junction_197 --end-id junction_209
Clearing existing TRAVELS_TO rels...
Creating new TRAVELS_TO rels...
TRAVELS_TO relationships created
Projecting in-memory graph...
Calculating shortest path...
Total distance: 4964 meters
Path: junction_197 -> junction_199 -> junction_29 -> junction_148 -> junction_139 -> junction_164 -> junction_147 -> junction_168 -> junction_209
Dropping in-memory graph projection...
```