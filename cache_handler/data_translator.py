import time
import json
import logging
from typing import Any, Dict, Iterator


logger = logging.getLogger('cache')


def json_relationships_satellites(relationships: Iterator[Dict[str, Any]]) -> "JSON":
    start_time = time.time()

    json_relationships = []
    json_satellites = []
    sat_ids = set()
    for rel in relationships:
        r = rel['r']
        s1 = rel['s1']
        s2 = rel['s2']

        json_relationships.append([s1.properties['x'], s1.properties['y'],
                                   s2.properties['x'], s2.properties['y'], r.properties['transmission_time']])

        if(not s1.properties['id'] in sat_ids):
            json_satellites.append(
                [s1.properties['id'], s1.properties['x'], s1.properties['y']])
            sat_ids.add(s1.properties['id'])
        if(not s2.properties['id'] in sat_ids):
            json_satellites.append(
                [s2.properties['id'], s2.properties['x'], s2.properties['y']])
            sat_ids.add(s2.properties['id'])

    logger.info(
        f'Relationship and Satellite JSON created in {time.time() - start_time} seconds.')
    return json.dumps(json_relationships), json.dumps(json_satellites)
