import os
import json
import time
import redis
import logging
import data_translator
from time import sleep
from typing import Dict, Any
from gqlalchemy import Memgraph


DB_FETCH_TIME = float(os.getenv('DB_FETCH_TIME', '0.5'))
MEMGRAPH_IP = os.getenv('MEMGRAPH_IP', 'memgraph')
MEMGRAPH_PORT = os.getenv('MEMGRAPH_PORT', '7687')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

logging.basicConfig(format='%(asctime)-15s [%(levelname)s]: %(message)s')
logger = logging.getLogger('cache')
logger.setLevel(logging.INFO)

# Wait for Redis and Memgraph to start
time.sleep(5)

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                      charset="utf-8", decode_responses=True)

def connect_to_memgraph(memgraph_ip, memgraph_port):
    memgraph = Memgraph(host=memgraph_ip, port=int(memgraph_port))
    while(True):
        try:
            if (memgraph._get_cached_connection().is_active()):
                return memgraph
        except:
            logger.info("Memgraph probably isn't running.")
            sleep(1)

db = connect_to_memgraph(MEMGRAPH_IP, MEMGRAPH_PORT)
results = {}

            
while(True):
    start_time = time.time()
        
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

    logger.info(f'Saved to cache in {time.time() - start_time} seconds.')
    time.sleep(DB_FETCH_TIME)
