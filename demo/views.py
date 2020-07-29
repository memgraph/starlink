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
    shortest_path = []
    json_shortest_path = []

    cities = db_connection.fetch_cities(db)
    satellites = db_connection.fetch_satellites(db)
    relationships = db_connection.fetch_relationships(db)
    shortest_path = db_connection.fetch_shortest_path(db, cities[0], cities[1])
    print(shortest_path)

    json_cities = json.dumps(db_connection.city_json_format(cities))
    json_satellites = json.dumps(
        db_connection.satellite_json_format(satellites))
    json_relationships = json.dumps(db_connection.relationship_json_format(relationships))
    json_shortest_path = json.dumps(db_connection.shortest_path_json_format(shortest_path))
    #print(json_shortest_path)
    #print(json_relationships)

    template = loader.get_template('demo/demo.html')
    return render(request, "demo/demo.html", {"city_markers": json_cities, "sat_markers": json_satellites, "rel_markers": json_relationships, "sp_markers:": json_shortest_path})


def postSatellitesAndRelationships(request):
    db = Memgraph()

    cities = []
    json_cities = []
    cities = db_connection.fetch_cities(db)
    json_cities = json.dumps(db_connection.city_json_format(cities))

    satellites = []
    json_satellites = []
    satellites = db_connection.fetch_satellites(db)
    json_satellites = json.dumps(db_connection.satellite_json_format(satellites))

    relationships = []
    json_relationships = []
    relationships = db_connection.fetch_relationships(db)
    json_relationships = json.dumps(db_connection.relationship_json_format(relationships))

    shortest_path = []
    json_shortest_path = []
    shortest_path = db_connection.fetch_shortest_path(db, cities[0], cities[1])
    json_shortest_path = json.dumps(db_connection.shortest_path_json_format(shortest_path))

    return JsonResponse({"json_cities": json_cities, "json_satellites": json_satellites, "json_relationships": json_relationships, "json_shortest_path": json_shortest_path}, status=200)


# Contents of this function are temporarily moved into above function until the ajax url problem is resolved
def postRelationships(request):
    db = Memgraph()

    relationships = []
    json_relationships = []
    relationships = db_connection.fetch_relationships(db)

    json_relationships = json.dumps(db_connection.relationship_json_format(relationships))

    return JsonResponse({"json_relationships": json_relationships}, status = 200)
