from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from pathlib import Path
from simulator.models import City, Orbit
from simulator import orbital_mechanics_utils
from simulator import db_operations
from simulator import setup
from skyfield.api import load as skyfield_load
from time import sleep
import numpy as np
import os
import time

_here = Path(__file__).parent

ts = skyfield_load.timescale(builtin=True)
minutes = np.arange(0,    24*60*5, 1)
time_of_simulation = ts.utc(2020, 7, 29, 0, minutes)
memgraph = None

TLE_FILE_PATH = os.getenv('TLE_FILE_PATH', 'imports/tle_1')
CITIES_FILE_PATH = os.getenv('CITIES_FILE_PATH', 'imports/cities.csv')
DB_UPDATE_TIME = float(os.getenv('DB_UPDATE_TIME', 0.1))
KAFKA_IP = os.getenv('KAFKA_IP', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
MEMGRAPH_IP = os.getenv('MEMGRAPH_IP', 'memgraph-mage')
MEMGRAPH_PORT = os.getenv('MEMGRAPH_PORT', '7687')


def create_kafka_producer():
    retries = 30
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_IP + ':' + KAFKA_PORT)
            return producer
        except NoBrokersAvailable:
            retries -= 1
            if not retries:
                raise
            print("Failed to connect to Kafka")
            sleep(1)


def set_up_memgraph_and_kafka():
    global memgraph
    memgraph = setup.connect_to_memgraph(MEMGRAPH_IP, MEMGRAPH_PORT)
    setup.run(memgraph, KAFKA_IP, KAFKA_PORT)


def run() -> None:

    set_up_memgraph_and_kafka()
    producer = create_kafka_producer()

    memgraph.drop_database()
    memgraph.execute("CREATE INDEX ON :City (id)")
    memgraph.execute("CREATE INDEX ON :Satellite (id)")

    tle_path = _here.parent.joinpath(TLE_FILE_PATH)
    ObjectsAndOrbits = orbital_mechanics_utils.generate_orbits_and_moving_objects(
        tle_path, time_of_simulation)

    cities_path = _here.parent.joinpath(CITIES_FILE_PATH)
    cities = City.generate_cities(cities_path, time_of_simulation)

    City.update_cities(cities, ObjectsAndOrbits.moving_objects_dict_by_id)

    Orbit.update_orbits(
        ObjectsAndOrbits.orbits_dict_by_id, ObjectsAndOrbits.moving_objects_dict_by_id)

    db_operations.create_data(producer=producer,
                              moving_objects_dict_by_id=ObjectsAndOrbits.moving_objects_dict_by_id,
                              cities=cities)

    while(True):
        Orbit.update_orbits(ObjectsAndOrbits.orbits_dict_by_id,
                            ObjectsAndOrbits.moving_objects_dict_by_id)
        City.update_cities(cities, ObjectsAndOrbits.moving_objects_dict_by_id)

        db_operations.update_data(producer=producer,
                                  moving_objects_dict_by_id=ObjectsAndOrbits.moving_objects_dict_by_id,
                                  cities=cities)
        time.sleep(DB_UPDATE_TIME)
        # time.sleep(200)
