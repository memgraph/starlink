import demo.utils as utils


def import_all_cities(db):
    command = "MATCH (n:City) RETURN n;"
    return db.execute_and_fetch(command)


def import_data(tx, city1, city2):
    print(f"{utils.bcolors.OKGREEN}Simulator DB update START{utils.bcolors.ENDC}")
          
    results = {}

    command = "MATCH (s:Satellite) RETURN s;"
    results[0] = tx.run(command) 

    command = "MATCH p=(c1:City { id: '" + str(city1) + \
        "'})-[rs *wShortest (e, n | e.transmission_time) total_transmission_time]-(c2:City { id: '" + str(
            city2) + "'}) RETURN nodes(p), rs;"
    results[2] = tx.run(command)

    command = "MATCH (s1:Satellite)-[r]-(s2:Satellite) RETURN r, s1, s2;"
    results[1] = tx.run(command)

    print(f"{utils.bcolors.OKGREEN}Simulator DB update END{utils.bcolors.ENDC}")

    return results