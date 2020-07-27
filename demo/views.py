from django.http import HttpResponse
from demo.database import Memgraph
import demo.data.db_operations as db_operations
from django.template import loader
from django.shortcuts import render 
import json


def index(request):

    db = Memgraph()
    satellites = db_operations.import_all_satellites(db)
    cities = db_operations.import_all_cities(db)

    sat_markers = []
    city_markers = []

    for sat in satellites:
        s = sat['n']
        marker = [s.properties['x'], s.properties['y']]
        sat_markers.append(marker)

    for city in cities:
        c = city['n']
        marker = [c.properties['x'], s.properties['y']]
        city_markers.append(marker)

    json_cities = json.dumps(city_markers)

    for i in json_cities:
        print(i)
    template = loader.get_template('demo/demo.html')
    context = {
        'city_markers': json_cities,
    }
    return render(request, "demo/demo.html", {"city_markers": json_cities}) 
