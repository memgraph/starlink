

def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)

def import_all_satellites(db):
        command = "MATCH (n :Satellite) RETURN n;"
        return db.execute_and_fetch(command)

def import_all_cities(db):
        command = "MATCH (n :City) RETURN n;"
        return db.execute_and_fetch(command)

def import_all_relationships(db):
        command = "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"
        return db.execute_and_fetch(command)

def establish_connection(db, city1, city2):
        command = "MATCH (s1:Satellite)-[r1]->(c1:City {id:'" + str(city1.id) + "'})" + \
        "MATCH (s2:Satellite)-[r2]->(c2:City {id:'" + str(city2.id) + "'})" + \
        "MATCH p=(:City { id: c1.id})-[r *wShortest (e, n | e.transmission_time) total_transmission_time]-(:City { id: c2.id})" + \
        "RETURN p;"
        db.execute_query(command)
        