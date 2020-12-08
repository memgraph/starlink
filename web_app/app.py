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
COMPRESS_MIN_SIZE = 300

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


@app.route('/')
def index() -> Any:
    start_time = time.time()

    cities = []
    optical_paths = []

    json_cities = []
    json_satellites = []
    json_relationships = []
    json_optical_paths = []

    results = {"relationships": [], "shortest_path": []}

    sys.excepthook = my_handler

    while len(cities) == 0:
        time.sleep(1)
        cities = db_connection.fetch_cities(db)

    optical_paths = OpticalPath.import_optical_paths(optical_path)

    results = db.execute_transaction(
        func=db_operations.import_sats_and_rels,
        arguments={})

    while len(results["relationships"]) == 0:
        time.sleep(0.1)
        results = db.execute_transaction(
            func=db_operations.import_sats_and_rels,
            arguments={})

    json_cities = db_connection.city_json_format(cities)
    json_optical_paths = db_connection.optical_paths_json_format(optical_paths)
    json_relationships, json_satellites = db_connection.json_relationships_satellites(results["relationships"])

    logger.info(
        f'Initial HTTP Request processed in {time.time() - start_time} seconds.')

    return render_template("demo.html", data={"city_markers": json_cities,
                                              "sat_markers": json_satellites,
                                              "rel_markers": json_relationships,
                                              "op_markers": json_optical_paths})


@app.route('/json_satellites_and_relationships', methods=["GET"])
def get_data() -> Any:
    start_time = time.time()

    json_satellites = []
    json_relationships = []
    json_shortest_path = []

    results = {"relationships": [], "shortest_path": []}

    while len(results["shortest_path"]) == 0 or len(results["relationships"]) == 0:
        time.sleep(0.1)
        results = db.execute_transaction(
            func=db_operations.import_data,
            arguments={"city_one": request.args.get('cityOne'),
                       "city_two": request.args.get('cityTwo')})

    json_relationships, json_satellites = db_connection.json_relationships_satellites(results["relationships"])
    json_shortest_path = db_connection.json_shortest_path(results["shortest_path"])
    
    logger.info(
        f'HTTP Request processed in {time.time() - start_time} seconds.')

    return {"json_satellites": json_satellites,
            "json_relationships": json_relationships,
            "json_shortest_path": json_shortest_path}


@app.route('/check', methods=["GET"])
def check() -> Any:
    """Route for AWS to check the status of the app"""
    return '', 200
