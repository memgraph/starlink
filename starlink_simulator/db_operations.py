

def init(db):
    file = open("starlink_simulator/create_db.txt")

    command = file.read().replace("\n", " ")
    file.close()

    db.execute_query(command)


def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)
