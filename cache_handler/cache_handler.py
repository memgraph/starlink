import os
import gc
import json
import time
import redis
import logging
import data_translator
from typing import Dict, Any
from database import Memgraph
import tracemalloc
import memory
import gc


DB_FETCH_TIME = float(os.getenv('DB_FETCH_TIME', '0.5'))
REDIS_HOST = os.getenv('REDIS_HOST', '172.18.0.2')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('cache')
logger.setLevel(logging.INFO)

# Wait for Redis and Memgraph to start
time.sleep(5)

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                      charset="utf-8", decode_responses=True)
db = Memgraph()

json_relationships = []
json_satellites = []
results = {}

while(True):
    tracemalloc.start()

    results["relationships"] = list(db.execute_and_fetch(
        "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"))
    while len(results["relationships"]) == 0:
        results["relationships"] = list(db.execute_and_fetch(
            "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"))
        time.sleep(1)

    json_relationships, json_satellites = data_translator.json_relationships_satellites(
        results["relationships"])

    r.set('json_relationships', json_relationships)
    r.set('json_satellites', json_satellites)

    logger.info(f'Saving to cache...')

    snapshot = tracemalloc.take_snapshot()
    memory.display_top(snapshot)
    time.sleep(DB_FETCH_TIME)
