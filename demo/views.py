from django.http import HttpResponse
from demo.database import Memgraph
import demo.data.db_operations as db_operations
from django.template import loader
from django.shortcuts import render
import json
from django.http import JsonResponse
import demo.data.db_connection as db_connection
import time
import demo.utils as utils
import starlink_simulator.orbital_mechanics_utils as omu


def index(request):

    time.sleep(2)
    db = Memgraph()
    #request.session['db'] = db

    json_satellites = []
    json_relationships = []
    json_shortest_path = []

    cities = db_connection.fetch_cities(db)
    optical_paths = omu.import_optical_paths()

    json_cities = json.dumps(db_connection.city_json_format(cities))
    json_optical_paths = json.dumps(db_connection.optical_paths_json_format(optical_paths))

    return render(request, "demo/demo.html", {"city_markers": json_cities, "sat_markers": json_satellites, "rel_markers": json_relationships, "sp_markers": json_shortest_path, "op_markers": json_optical_paths})


def postSatellitesAndRelationships(request):

    db = Memgraph()
    #db = request.session['db']

    satellites = []
    relationships = []
    shortest_path = []

    json_satellites = []
    json_relationships = []
    json_shortest_path = []

    results = db.execute_transaction(db_operations.import_data, request.GET.get(
        'cityOne', None), request.GET.get('cityTwo', None))

    satellites = db_connection.transform_satellites(results[0])
    relationships = db_connection.transform_relationships(results[1])
    shortest_path = db_connection.transform_shortest_path(results[2])

    json_satellites = json.dumps(
        db_connection.satellite_json_format(satellites))

    json_relationships = json.dumps(
        db_connection.relationship_json_format(relationships))

    if (shortest_path != 0):
        json_shortest_path = json.dumps(
            db_connection.shortest_path_json_format(shortest_path))

    return JsonResponse({"json_satellites": json_satellites, "json_relationships": json_relationships, "json_shortest_path": json_shortest_path}, status=200)
