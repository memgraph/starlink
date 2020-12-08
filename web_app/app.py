import time
import json
import os
import logging
import sys
#import redis
from flask import Flask, render_template, request, jsonify, make_response
from flask_compress import Compress
from demo.database import Memgraph
from demo.data import db_operations, db_connection, OpticalPath
from pathlib import Path
from typing import Any, List


COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                      'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('web')
logger.setLevel(logging.INFO)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

_here = Path(__file__)

app = Flask(__name__)
Compress(app)

db = Memgraph()

OPTICAL_FILE_PATH = os.getenv(
    'OPTICAL_FILE_PATH', 'resources/latencies.csv')
optical_path = _here.parent.joinpath(OPTICAL_FILE_PATH)


def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))


#REDIS_HOST = os.getenv('REDIS_HOST', '172.18.0.2')
#REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

# r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
#                      charset="utf-8", decode_responses=True)


@app.route('/')
def index() -> Any:
    cities = []
    satellites = []
    relationships = []
    optical_paths = []

    json_cities = []
    json_satellites = []
    json_relationships = []
    json_optical_paths = []

    results = {"satellites": [], "relationships": [], "shortest_path": []}

    sys.excepthook = my_handler

    while len(cities) == 0:
        time.sleep(1)
        cities = db_connection.fetch_cities(db)

    optical_paths = OpticalPath.import_optical_paths(optical_path)

    results = db.execute_transaction(
        func=db_operations.import_sats_and_rels,
        arguments={})

    while len(results["satellites"]) == 0 or len(results["relationships"]) == 0:
        time.sleep(1)
        results = db.execute_transaction(
            func=db_operations.import_sats_and_rels,
            arguments={})

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
def get_data() -> Any:
    satellites = []
    relationships = []
    shortest_path = []

    json_satellites = []
    json_relationships = []
    json_shortest_path = []

    results = {"satellites": [], "relationships": [], "shortest_path": []}

    while len(results["satellites"]) == 0 or len(results["shortest_path"]) == 0 or len(results["relationships"]) == 0:
        results = db.execute_transaction(
            func=db_operations.import_data,
            arguments={"city_one": request.args.get('cityOne'),
                       "city_two": request.args.get('cityTwo')})

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

    #json_relationships = r.get('relationships')

    return {"json_satellites": json_satellites,
            "json_relationships": json_relationships,
            "json_shortest_path": json_shortest_path}


@app.route('/check', methods=["GET"])
def check() -> Any:
    """Route for AWS to check the status of the app"""
    return '', 200
