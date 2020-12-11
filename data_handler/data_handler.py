from typing import Dict, Any
import logging
import os
import json
import time
import redis
from database import Memgraph, connection
from data import db_operations, db_connection


DB_FETCH_TIME = float(os.getenv('DB_FETCH_TIME', '0.5'))
REDIS_HOST = os.getenv('REDIS_HOST', '172.18.0.2')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))


logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('data_handler')
logger.setLevel(logging.INFO)

# Wait for Redis and Memgraph to start
time.sleep(5)

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                      charset="utf-8", decode_responses=True)
db = Memgraph()

results = {"relationships": []}
relationships = []
json_relationships = []

while(True):
    while len(results["relationships"]) == 0:
        results = db.execute_transaction(
            func=db_operations.import_rels,
            arguments={})
        time.sleep(1)

    json_relationships, json_satellites = db_connection.json_relationships_satellites(
        results["relationships"])

    r.set('json_relationships', json_relationships)
    r.set('json_satellites', json_satellites)

    results = {"relationships": []}

    logger.info(f'Saving to cache...')

    time.sleep(DB_FETCH_TIME)
