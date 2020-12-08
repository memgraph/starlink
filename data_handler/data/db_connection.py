import data.db_operations as db_operations
from database import Memgraph
from data.model import Relationship
from typing import Any, List


def transform_relationships(relationships: Any) -> List[Relationship]:
    relations = []
    for rel in relationships:
        r = rel['r']
        s1 = rel['s1']
        s2 = rel['s2']
        rel_obj = Relationship(s1.properties['x'], s1.properties['y'],
                               s2.properties['x'], s2.properties['y'],
                               r.properties['transmission_time'])
        relations.append(rel_obj)
    return relations


def relationship_json_format(relationships: List[Relationship]) -> List[Any]:
    json_relationships = []
    for r in relationships:
        json_relationships.append(
            [r.xS, r.yS, r.xE, r.yE, r.transmission_time])
    return json_relationships
