import json
from django.contrib.gis.geos import MultiLineString, LineString
import polyline
from postgis_app.models import Route


with open('/app/scripts/rms.json', 'r') as f:
    featurecollection = json.load(f)

for feature in featurecollection['features']:
    properties = feature['properties']

    print(properties.get('type'))

    if properties.get('type') == 'trail':
        geometry = feature['geometry']

        try:
            coordinates = polyline.decode(geometry['encodedpath'])
        except IndexError:
            print(f'Something odd about {properties["name"]}')
            print(geometry['encodedpath'])

        route = Route.objects.create(
            name=properties['name'],
            geometry=MultiLineString(LineString([c[::-1] for c in coordinates]))
        )