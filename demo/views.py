from django.http import HttpResponse
from demo.database import Memgraph
import demo.data.db_operations as db_operations
from django.template import loader
from django.shortcuts import render 
import json
import demo.data.db_connection as db_connection

def index(request):
    db = Memgraph()

 #   sat_markers = db_connection.fetch_satellites(db)
    city_markers = db_connection.fetch_cities(db)

    json_cities = json.dumps(city_markers)
    json_satellites = json.dumps(sat_markers)

    #for i in json_cities:
    #    print(i)
    template = loader.get_template('demo/demo.html')
    context = {
        'city_markers': json_cities,
    }
    return render(request, "demo/demo.html", {"city_markers": json_cities, "sat_markers": json_satellites}) 
