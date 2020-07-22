

def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)


def update_object_positions(db, all_moving_objects_dict):
    command = "MATCH (n { id: 'Andy' }) SET n.age = toString(n.age)"
    db.execute_query(command)


def create_moving_objects(db, all_moving_objects):
    for moving_object in all_moving_objects:
        command = "CREATE (n:Satellite {id:'" + str(moving_object.id) + "', x:" + str(
            moving_object.x) + ", y:" + str(moving_object.y) + ", z:" + str(moving_object.z) + "})"
        db.execute_query(command)


def create_cities(db, cities):
    for city in cities:
        command = "CREATE (n:City {id:'" + str(city.id) + "', name:'" + str(
            city.name) + "', x:" + str(city.x) + ", y:" + str(city.y) + "})"
        db.execute_query(command)


def create_laser_connections(db, all_moving_objects):
    for moving_object_a in all_moving_objects:
        command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object_a.laser_left_id) + "' AND a.id = '" + str(moving_object_a.id) + \
            "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
            str(moving_object_a.laser_left_distance) + " }]->(b)"
        db.execute_query(command)
        
        command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object_a.laser_right_id) + "' AND a.id = '" + str(moving_object_a.id) + \
            "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
            str(moving_object_a.laser_right_distance) + " }]->(b)"
        db.execute_query(command)

        command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object_a.laser_up_id) + "' AND a.id = '" + str(moving_object_a.id) + \
            "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
            str(moving_object_a.laser_up_distance) + " }]->(b)"
        db.execute_query(command)

        command = "MATCH (a:Satellite),(b:Satellite) WHERE b.id = '" + str(moving_object_a.laser_down_id) + "' AND a.id = '" + str(moving_object_a.id) + \
            "' CREATE (a)-[r:CONNECTED_TO { transmission_time: " + \
            str(moving_object_a.laser_down_distance) + " }]->(b)"
        db.execute_query(command)
