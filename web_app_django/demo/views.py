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
import pickle


def index(request):

    db = Memgraph()
    request.session['db'] = pickle.dumps(db)

    json_satellites = []
    json_relationships = []

    cities = []
    while len(cities) == 0:
        time.sleep(1)
        cities = db_connection.fetch_cities(db)
    optical_paths = utils.import_optical_paths()

    results = db.execute_transaction(db_operations.import_sats_and_rels, [])
    while len(results["satellites"]) == 0:
        time.sleep(1)
        results = db.execute_transaction(db_operations.import_sats_and_rels, [])

    satellites = db_connection.transform_satellites(results["satellites"])
    relationships = db_connection.transform_relationships(results["relationships"])

    json_cities = json.dumps(db_connection.city_json_format(cities))
    json_satellites = json.dumps(db_connection.satellite_json_format(satellites))
    json_relationships = json.dumps(db_connection.relationship_json_format(relationships))
    json_optical_paths = json.dumps(
        db_connection.optical_paths_json_format(optical_paths))
    
    return render(request, "demo/demo.html", {"city_markers": json_cities, 
                                                "sat_markers": json_satellites, 
                                                "rel_markers": json_relationships,
                                                "op_markers": json_optical_paths})


def postSatellitesAndRelationships(request):

    db = pickle.loads(request.session['db'])

    satellites = []
    relationships = []
    shortest_path = []

    json_satellites = []
    json_relationships = []
    json_shortest_path = []

    results = db.execute_transaction(db_operations.import_data, [request.GET.get(
        'cityOne', None), request.GET.get('cityTwo', None)])

    satellites = db_connection.transform_satellites(results["satellites"])
    relationships = db_connection.transform_relationships(results["relationships"])
    shortest_path = db_connection.transform_shortest_path(results["shortest_path"])

    json_satellites = json.dumps(
        db_connection.satellite_json_format(satellites))

    json_relationships = json.dumps(
        db_connection.relationship_json_format(relationships))

    if (shortest_path != 0):
        json_shortest_path = json.dumps(
            db_connection.shortest_path_json_format(shortest_path))

    return JsonResponse({"json_satellites": json_satellites, 
                        "json_relationships": json_relationships, 
                        "json_shortest_path": json_shortest_path}, status=200)


def check(request):
    return HttpResponse(status=200)