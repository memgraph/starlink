from __future__ import annotations
import os
import csv
import math as m
import logging
from dataclasses import dataclass, field
from pathlib import Path
from simulator.models.moving_object import MovingObject
from simulator.models.stationary_object import StationaryObject
from skyfield.api import Topos
from typing import List, Dict, Any


logger = logging.getLogger('simulator')

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
                dist = City.eci_distance(
                    self, moving_objects_dict_by_id[moving_object_id])
                self.moving_objects_distances_dict[moving_object_id] = dist
                self.moving_objects_tt_dict[moving_object_id] = dist * \
                    1000/V_RADIO + RELAY_PROCESSING_DELAY

    @staticmethod
    def update_cities(cities: List[City], moving_objects_dict_by_id: Dict[int, MovingObject]) -> None:
        for city in cities:
            city.update_position()

        for city in cities:
            city.city_visible_moving_object_distances(
                moving_objects_dict_by_id)

    @staticmethod
    def generate_cities(file_path: Path, time: Any) -> List[City]:
        cities = []
        logger.info(f'Reading cities from file path {file_path}...')
        with file_path.open() as f:
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
    def eci_distance(city: City, moving_object: MovingObject) -> float:
        return m.sqrt((city.eci_x - moving_object.eci_x)**2 +
                      (city.eci_y - moving_object.eci_y)**2 +
                      (city.eci_z - moving_object.eci_z)**2)

    @staticmethod
    def calculate_angle(city: City, moving_object: MovingObject) -> float:
        angle = m.acos(
            moving_object.z / City.eci_distance(moving_object, city)) * 180.0/m.pi
        return angle
