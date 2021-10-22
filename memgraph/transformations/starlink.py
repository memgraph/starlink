import mgp
import json


@mgp.transformation
def satellite(messages: mgp.Messages
              ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        json_message = json.loads(message.payload().decode('utf8'))
        # print(json_message)
        result_queries.append(
            mgp.Record(
                query=("MERGE (s:Satellite { id: toString($id) }) "
                       "SET s.x = toFloat($x), "
                       "s.y=toFloat($y), "
                       "s.z=toFloat($z);"),
                parameters={
                    "id": json_message["id"],
                    "x": json_message["x"],
                    "y": json_message["y"],
                    "z": json_message["z"]}))

    return result_queries


@mgp.transformation
def city(messages: mgp.Messages
         ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        json_message = json.loads(message.payload().decode('utf8'))
        # print(json_message)
        result_queries.append(
            mgp.Record(
                query=("MERGE (s:City { id: toString($id) }) "
                       "SET s.name = toString($name), "
                       "s.x=toFloat($x), "
                       "s.y=toFloat($y);"),
                parameters={
                    "id": json_message["id"],
                    "name": json_message["name"],
                    "x": json_message["x"],
                    "y": json_message["y"]}))

    return result_queries


@mgp.transformation
def visible_from(messages: mgp.Messages
                 ) -> mgp.Record(query=str,
                                 parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        json_message = json.loads(message.payload().decode('utf8'))
        # print(json_message)
        result_queries.append(
            mgp.Record(
                query=("MATCH (c:City { id: toString($city_id)}), (s:Satellite { id: toString($satellite_id) }) "
                       "CREATE (s)-[r:VISIBLE_FROM { transmission_time: toFloat($transmission_time) }]->(c);"),
                parameters={
                    "city_id": json_message["city_id"],
                    "satellite_id": json_message["satellite_id"],
                    "transmission_time": json_message["transmission_time"]}))

    return result_queries


@mgp.transformation
def delete_visible_from(messages: mgp.Messages
                        ) -> mgp.Record(query=str,
                                        parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        json_message = json.loads(message.payload().decode('utf8'))
        # print(json_message)
        result_queries.append(
            mgp.Record(
                query=(
                    "MATCH (:Satellite)-[r]->(:City { id: toString($id) }) DELETE r;"),
                parameters={
                    "id": json_message["id"]}))

    return result_queries


@mgp.transformation
def laser_link(messages: mgp.Messages
               ) -> mgp.Record(query=str,
                               parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        json_message = json.loads(message.payload().decode('utf8'))
        # print(json_message)
        result_queries.append(
            mgp.Record(
                query=("MATCH (a: Satellite { id: toString($laser_id) }), (b: Satellite { id: toString($moving_object_id) }) "
                       "MERGE (a)-[c:CONNECTED_TO]->(b) "
                       "SET c.transmission_time = toFloat($laser_transmission_time);"),
                parameters={
                    "laser_id": json_message["laser_id"],
                    "moving_object_id": json_message["moving_object_id"],
                    "laser_transmission_time": json_message["laser_transmission_time"]}))

    return result_queries
