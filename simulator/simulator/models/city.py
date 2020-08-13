import os
import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from simulator.models.stationary_object import StationaryObject
from simulator import utils
from skyfield.api import Topos


V_RADIO = 2.99792458E+8
RELAY_PROCESSING_DELAY = float(os.getenv('RELAY_PROCESSING_DELAY', 0))
VIEW_ANGLE = float(os.getenv('VIEW_ANGLE', 70))


@dataclass
class City(StationaryObject):
    name: str

    def __post_init__(self):
        StationaryObject.__post_init__(self)
        self.moving_objects_distances_dict = {}
        self.moving_objects_tt_dict = {}

    def city_visible_moving_object_distances(self, moving_objects_dict_by_id):
        self.moving_objects_distances_dict = {}
        self.moving_objects_tt_dict = {}
        for moving_object_id in moving_objects_dict_by_id.keys():
            angle = City.calculate_angle(
                self, moving_objects_dict_by_id[moving_object_id])

            if angle <= VIEW_ANGLE:
                dist = utils.eci_distance(
                    self, moving_objects_dict_by_id[moving_object_id])
                self.moving_objects_distances_dict[moving_object_id] = dist
                self.moving_objects_tt_dict[moving_object_id] = dist * \
                    1000/V_RADIO + RELAY_PROCESSING_DELAY

    @staticmethod
    def update_city_positions(cities):
        for city in cities:
            city.update_position()

    @staticmethod
    def update_city_moving_object_distances(cities, moving_objects_dict_by_id):
        for city in cities:
            city.city_visible_moving_object_distances(
                moving_objects_dict_by_id)

    @staticmethod
    def generate_cities(file_path, time):
        cities = []
        path = Path(__file__).parent.parent.parent / file_path
        with path.open() as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:

                topos = Topos(latitude_degrees=float(row['latitude']),
                              longitude_degrees=float(row['longitude']),
                              elevation_m=float(row['altitude']))

                geocentric = topos.at(time)

                city = City(id=row['id'],
                            x=topos.latitude.degrees,
                            y=topos.longitude.degrees,
                            z=topos.elevation.km,
                            eci_x_positions=geocentric.position.km[0],
                            eci_y_positions=geocentric.position.km[1],
                            eci_z_positions=geocentric.position.km[2],
                            name=row['name'])

                cities.append(city)
        return cities

    @staticmethod
    def calculate_angle(city, moving_object):
        angle = math.acos(
            moving_object.z / utils.eci_distance(moving_object, city)) * 180.0/math.pi

        return angle
