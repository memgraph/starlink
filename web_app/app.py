import os
import sys
import time
import json
import redis
import logging
from pathlib import Path
from demo.database import Memgraph
from flask_compress import Compress
from demo import db_operations, data_translator
from flask import Flask, render_template, request, jsonify, make_response


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

OPTICAL_FILE_PATH = _here.parent.joinpath(os.getenv(
    'OPTICAL_FILE_PATH', 'resources/latencies.csv'))


def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))


REDIS_HOST = os.getenv('REDIS_HOST', '172.18.0.2')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                      charset="utf-8", decode_responses=True)


@app.route('/')
def index():
    start_time = time.time()

    json_cities = []
    json_satellites = []
    json_relationships = []
    json_optical_paths = []

    results = {"relationships": [], "shortest_path": []}

    sys.excepthook = my_handler

    results = db.execute_transaction(
        func=db_operations.import_satellites_and_relationships,
        arguments={})

    while len(results["relationships"]) == 0:
        time.sleep(0.1)
        results = db.execute_transaction(
            func=db_operations.import_satellites_and_relationships,
            arguments={})

    json_cities = data_translator.json_cities(db)
    json_optical_paths = data_translator.json_optical_paths(OPTICAL_FILE_PATH)
    json_relationships, json_satellites = data_translator.json_relationships_satellites(
        results["relationships"])

    logger.info(
        f'Initial HTTP Request processed in {time.time() - start_time} seconds.')

    return render_template("demo.html", data={"city_markers": json_cities,
                                              "sat_markers": json_satellites,
                                              "rel_markers": json_relationships,
                                              "op_markers": json_optical_paths})


@app.route('/json_satellites_and_relationships', methods=["GET"])
def get_data():
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

    json_relationships = r.get('json_relationships')
    json_satellites = r.get('json_satellites')
    json_shortest_path = data_translator.json_shortest_path(
        results["shortest_path"])

    logger.info(
        f'HTTP Request processed in {time.time() - start_time} seconds.')

    return {"json_satellites": json_satellites,
            "json_relationships": json_relationships,
            "json_shortest_path": json_shortest_path}


@app.route('/check', methods=["GET"])
def check():
    """Route for AWS to check the status of the app"""
    return '', 200
