from flask import Flask, render_template, request, jsonify, make_response
from flask_caching import Cache
from demo.database import Memgraph
from demo.data import db_operations, db_connection
from demo import utils
import pickle
import time
import json
import os

config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/')
def index():
    db = Memgraph()
    cache.set('db', db)

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
        results = db.execute_transaction(
            db_operations.import_sats_and_rels, [])

    satellites = db_connection.transform_satellites(results["satellites"])
    relationships = db_connection.transform_relationships(
        results["relationships"])

    json_cities = db_connection.city_json_format(cities)
    json_satellites = db_connection.satellite_json_format(satellites)
    json_relationships = db_connection.relationship_json_format(relationships)
    json_optical_paths = db_connection.optical_paths_json_format(optical_paths)

    return render_template("demo.html", data={"city_markers": json_cities,
                                              "sat_markers": json_satellites,
                                              "rel_markers": json_relationships,
                                              "op_markers": json_optical_paths})


@app.route('/json_satellites_and_relationships', methods=["GET"])
def postSatellitesAndRelationships():

    db = cache.get('db')

    satellites = []
    relationships = []
    shortest_path = []

    json_satellites = []
    json_relationships = []
    json_shortest_path = []

    results = db.execute_transaction(db_operations.import_data, [
                                     request.args.get('cityOne'), request.args.get('cityTwo')])

    satellites = db_connection.transform_satellites(results["satellites"])
    relationships = db_connection.transform_relationships(
        results["relationships"])
    shortest_path = db_connection.transform_shortest_path(
        results["shortest_path"])

    json_satellites = json.dumps(
        db_connection.satellite_json_format(satellites))

    json_relationships = json.dumps(
        db_connection.relationship_json_format(relationships))

    if (shortest_path != 0):
        json_shortest_path = json.dumps(
            db_connection.shortest_path_json_format(shortest_path))

    return {"json_satellites": json_satellites,
            "json_relationships": json_relationships,
            "json_shortest_path": json_shortest_path}


@app.route('/check', methods=["GET"])
def check():
    return '', 200
