import logging
from simulator.database import Memgraph
from simulator.models import City, MovingObject, Orbit
from typing import List, Dict, Any


logger = logging.getLogger('simulator')


def create_laser_command(moving_object_id: int,
                         laser_id: int,
                         laser_transmission_time: float):
    command = (f'MATCH (a: Satellite), (b: Satellite) WHERE b.id = "{laser_id}" AND a.id = "{moving_object_id}"\
                 CREATE(a)-[r:CONNECTED_TO {{transmission_time: {laser_transmission_time}}}] -> (b)')
    return command


def update_laser_command(moving_object_id: int,
                         laser_id: int,
                         laser_transmission_time: float):
    command = (f'MATCH (a: Satellite {{id:"{moving_object_id}"}})-[r]-(b: Satellite {{id:"{laser_id}"}})\
                 SET r.transmission_time = {laser_transmission_time}')
    return command


def create_data(tx: Any,
                moving_objects_dict_by_id: Dict[id, MovingObject],
                cities: List[City]) -> None:
    tx.run("BEGIN")

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        command = (
            f'CREATE(n: Satellite {{id: "{moving_object.id}",\
                                    x: {moving_object.x},\
                                    y: {moving_object.y},\
                                    z: {moving_object.z}}})')
        tx.run(command)

    for city in cities:
        command = (
            f'CREATE(n: City {{id: "{city.id}",\
                               name: " {city.name}",\
                               x: {city.x},\
                               y: {city.y}}})')
        tx.run(command)

    for city in cities:
        for key in city.moving_objects_tt_dict:
            command = (
                f'MATCH (a:City {{ id:" {city.id} "}}), (b:Satellite) WHERE b.id = "{key}" \
                  CREATE (b)-[r:VISIBLE_FROM {{ transmission_time: {city.moving_objects_tt_dict[key]} }}]->(a)')
            tx.run(command)

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]

        command = create_laser_command(
            moving_object.id, moving_object.laser_left_id, moving_object.laser_left_transmission_time)
        tx.run(command)

        command = create_laser_command(
            moving_object.id, moving_object.laser_right_id, moving_object.laser_right_transmission_time)
        tx.run(command)

        command = create_laser_command(
            moving_object.id, moving_object.laser_up_id, moving_object.laser_up_transmission_time)
        tx.run(command)

        command = create_laser_command(
            moving_object.id, moving_object.laser_down_id, moving_object.laser_down_transmission_time)
        tx.run(command)

    #logger.info('Commiting initial DB transaction...')
    tx.run("COMMIT")
    

def update_data(tx: Any,
                moving_objects_dict_by_id: Dict[id, MovingObject],
                cities: List[City]) -> None:
    tx.run("BEGIN")

    for city in cities:
        command = (
            f'MATCH (b:Satellite)-[r]->(a:City {{id: "{city.id}"}}) DELETE r')
        tx.run(command)

        for key in city.moving_objects_tt_dict:
            command = (
                f'MATCH (a:City {{ id: "{city.id}"}}),(b:Satellite) WHERE b.id = "{key}" \
                  CREATE (b)-[r:VISIBLE_FROM {{ transmission_time: {city.moving_objects_tt_dict[key]} }}]->(a)')
            tx.run(command)

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        command = (
            f'MATCH (a:Satellite {{ id:"{moving_object.id}"}}) \
              SET a.x = {moving_object.x},\
                  a.y = {moving_object.y},\
                  a.z = {moving_object.z}')
        tx.run(command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_left_id, moving_object.laser_left_transmission_time)
        tx.run(command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_right_id, moving_object.laser_right_transmission_time)
        tx.run(command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_up_id, moving_object.laser_up_transmission_time)
        tx.run(command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_down_id, moving_object.laser_down_transmission_time)
        tx.run(command)

    tx.run("COMMIT")


def clear(db: Memgraph) -> None:
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)
