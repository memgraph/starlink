import time
import json
import logging
from typing import Any, Dict, Iterator


logger = logging.getLogger("cache")


def json_relationships_satellites(relationships: Iterator[Dict[str, Any]]) -> "JSON":
    start_time = time.time()

    json_relationships = []
    json_satellites = {}
    sat_ids = set()
    for rel in relationships:
        r = rel["r"]
        s1 = rel["s1"]
        s2 = rel["s2"]
        print(rel)
        json_relationships.append([s1.x, s1.y, s2.x, s2.y, r.transmission_time])

        if not s1.id in sat_ids:
            json_satellites[s1.id] = [
                s1.x,
                s1.y,
            ]
            sat_ids.add(s1.id)
        if not s2.id in sat_ids:
            json_satellites[s2.id] = [
                s2.x,
                s2.y,
            ]
            sat_ids.add(s2.id)

    logger.info(
        f"Relationship and Satellite JSON created in {time.time() - start_time} seconds."
    )
    return json.dumps(json_relationships), json.dumps(json_satellites)
