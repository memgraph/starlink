def clear(db):
    command = "MATCH (node) DETACH DELETE node"
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


def update_object_positions(db, all_moving_objects):
    for moving_object in all_moving_objects:
        command = "MATCH (a:Satellite { id:'" + str(moving_object.id) + "'}) SET a.x=" + str(
            moving_object.x) + ", a.y=" + str(moving_object.y) + ", a.z=" + str(moving_object.z)
        db.execute_query(command)


def create_city_moving_objects_visibility(db, cities, all_moving_objects):
    for city in cities:
        command = "MATCH (a:City { id:'" + str(city.id) + "'}),(b:Satellite) WHERE b.id = '" + str(min(city.moving_objects_distances_dict, key=city.moving_objects_distances_dict.get)) + \
            "' CREATE (b)-[r:VISIBLE_FROM { transmission_time: " + \
            str(city.moving_objects_distances_dict[min(city.moving_objects_distances_dict, key=city.moving_objects_distances_dict.get)]) + " }]->(a)"
        db.execute_query(command)

def update_city_moving_objects_visibility(db, cities, all_moving_objects):
    for city in cities:
        command = "MATCH (b:Satellite)-[r]->(a:City {id:'" + str(city.id) + "'}) DELETE r"
        db.execute_query(command)
        command = "MATCH (a:City { id:'" + str(city.id) + "'}),(b:Satellite) WHERE b.id = '" + str(min(city.moving_objects_distances_dict, key=city.moving_objects_distances_dict.get)) + \
            "' CREATE (b)-[r:VISIBLE_FROM { transmission_time: " + \
            str(city.moving_objects_distances_dict[min(city.moving_objects_distances_dict, key=city.moving_objects_distances_dict.get)]) + " }]->(a)"
        db.execute_query(command)
    #create_city_moving_objects_visibility(db, cities, all_moving_objects)
      

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


def update_laser_connections(db, all_moving_objects):
    for moving_object_a in all_moving_objects:
        command = "MATCH (a:Satellite {id:'" + str(moving_object_a.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object_a.laser_left_id) + "'})" + \
            " SET r.transmission_time=" + \
            str(moving_object_a.laser_left_distance)
        db.execute_query(command)

        command = "MATCH (a:Satellite {id:'" + str(moving_object_a.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object_a.laser_right_id) + "'})" + \
            " SET r.transmission_time=" + \
            str(moving_object_a.laser_right_distance)
        db.execute_query(command)

        command = "MATCH (a:Satellite {id:'" + str(moving_object_a.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object_a.laser_up_id) + "'})" + \
            " SET r.transmission_time=" + \
            str(moving_object_a.laser_up_distance)
        db.execute_query(command)

        command = "MATCH (a:Satellite {id:'" + str(moving_object_a.id) + "'})-[r]-(b:Satellite {id:'" + str(moving_object_a.laser_down_id) + "'})" + \
            " SET r.transmission_time=" + \
            str(moving_object_a.laser_down_distance)
        db.execute_query(command)
