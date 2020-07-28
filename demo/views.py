from django.http import HttpResponse
from demo.database import Memgraph
import demo.data.db_operations as db_operations
from django.template import loader
from django.shortcuts import render
import json
from django.http import JsonResponse
import demo.data.db_connection as db_connection


def index(request):
    db = Memgraph()

    cities = []
    satellites = []
    json_cities = []
    json_satellites = []

    cities = db_connection.fetch_cities(db)
    satellites = db_connection.fetch_satellites(db)
    db_connection.print_shortestpath(db)

    json_cities = json.dumps(db_connection.city_json_format(cities))
    json_satellites = json.dumps(
        db_connection.satellite_json_format(satellites))

    template = loader.get_template('demo/demo.html')
    return render(request, "demo/demo.html", {"city_markers": json_cities, "sat_markers": json_satellites})


def postSatellites(request):
    db = Memgraph()

    satellites = []
    json_satellites = []

    satellites = db_connection.fetch_satellites(db)

    json_satellites = json.dumps(
        db_connection.satellite_json_format(satellites))

    return JsonResponse({"json_satellites": json_satellites}, status=200)