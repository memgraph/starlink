from simulator.database import Memgraph
from simulator.database.connection import _convert_memgraph_value 
from typing import List, Dict, Any, Iterator


def clear(db: Memgraph) -> None:
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)


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


def create_data(cursor: Any, arguments: Dict[str, Any]) -> None:
    moving_objects_dict_by_id = arguments["moving_objects_dict_by_id"]
    cities = arguments["cities"]

    execute_transaction_query(cursor, "BEGIN")

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        command = (
            f'CREATE(n: Satellite {{id: "{moving_object.id}",\
                                    x: {moving_object.x},\
                                    y: {moving_object.y},\
                                    z: {moving_object.z}}})')
        execute_transaction_query(cursor, command)

    for city in cities:
        command = (
            f'CREATE(n: City {{id: "{city.id}",\
                               name: "{city.name}",\
                               x: {city.x},\
                               y: {city.y}}})')
        execute_transaction_query(cursor, command)

    for city in cities:
        for key in city.moving_objects_tt_dict:
            command = (
                f'MATCH (a:City {{ id:" {city.id} "}}), (b:Satellite) WHERE b.id = "{key}" \
                  CREATE (b)-[r:VISIBLE_FROM {{ transmission_time: {city.moving_objects_tt_dict[key]} }}]->(a)')
            execute_transaction_query(cursor, command)

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]

        command = create_laser_command(
            moving_object.id, moving_object.laser_left_id, moving_object.laser_left_transmission_time)
        execute_transaction_query(cursor, command)

        command = create_laser_command(
            moving_object.id, moving_object.laser_right_id, moving_object.laser_right_transmission_time)
        execute_transaction_query(cursor, command)

        command = create_laser_command(
            moving_object.id, moving_object.laser_up_id, moving_object.laser_up_transmission_time)
        execute_transaction_query(cursor, command)

        command = create_laser_command(
            moving_object.id, moving_object.laser_down_id, moving_object.laser_down_transmission_time)
        execute_transaction_query(cursor, command)

    execute_transaction_query(cursor, "COMMIT")
    return {}


def update_data(cursor: Any, arguments: Dict[str, Any]) -> None:
    moving_objects_dict_by_id = arguments["moving_objects_dict_by_id"]
    cities = arguments["cities"]

    execute_transaction_query(cursor, "BEGIN")
    
    for city in cities:
        command = (
            f'MATCH (b:Satellite)-[r]->(a:City {{id: "{city.id}"}}) DELETE r')
        execute_transaction_query(cursor, command)

        for key in city.moving_objects_tt_dict:
            command = (
                f'MATCH (a:City {{ id: "{city.id}"}}),(b:Satellite) WHERE b.id = "{key}" \
                  CREATE (b)-[r:VISIBLE_FROM {{ transmission_time: {city.moving_objects_tt_dict[key]} }}]->(a)')
            execute_transaction_query(cursor, command)

    for moving_object_id in moving_objects_dict_by_id.keys():
        moving_object = moving_objects_dict_by_id[moving_object_id]
        command = (
            f'MATCH (a:Satellite {{ id:"{moving_object.id}"}}) \
              SET a.x = {moving_object.x},\
                  a.y = {moving_object.y},\
                  a.z = {moving_object.z}')
        execute_transaction_query(cursor, command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_left_id, moving_object.laser_left_transmission_time)
        execute_transaction_query(cursor, command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_right_id, moving_object.laser_right_transmission_time)
        execute_transaction_query(cursor, command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_up_id, moving_object.laser_up_transmission_time)
        execute_transaction_query(cursor, command)

        command = update_laser_command(
            moving_object.id, moving_object.laser_down_id, moving_object.laser_down_transmission_time)
        execute_transaction_query(cursor, command)

    execute_transaction_query(cursor, "COMMIT")
    return {}


def execute_transaction_query(cursor: Any, query: str) -> None:
    try:
        cursor.execute(query)
        cursor.fetchall()
    except:
        print("Something went wrong with the transaction read query")


def execute_transaction_query_and_fetch(cursor: Any, query: str) -> Iterator[Dict[str, Any]]:
        output = []
        try:
            cursor.execute(query)
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                output.append({
                            dsc.name: _convert_memgraph_value(row[index])
                            for index, dsc in enumerate(cursor.description)})
        except:
            print("Something went wrong with the transaction write query")
        return output
