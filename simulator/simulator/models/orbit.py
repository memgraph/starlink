from __future__ import annotations
import os
from dataclasses import dataclass, field
from simulator.models.moving_object import MovingObject
from typing import List, Dict


V_LASER_VACUUM = 2.99792458E+8
SAT_PROCESSING_DELAY = float(os.getenv('SAT_PROCESSING_DELAY', 0))


@dataclass
class Orbit:
    id: int

    def __post_init__(self):
        self.moving_objects = []

    def add_object(self, moving_object: MovingObject) -> None:
        self.moving_objects.append(moving_object)

    def update_moving_object_positions(self) -> None:
        for moving_object in self.moving_objects:
            moving_object.current_position += 1
            if (moving_object.current_position == moving_object.positions_lenght):
                moving_object.current_position = 0

            moving_object.updatePosition()

    def update_laser_connections(self, orbits_dict_by_id: Dict[id, Orbit]) -> None:
        for moving_object in self.moving_objects:
            moving_object.update_laser_up(orbits_dict_by_id)
            moving_object.update_laser_down(orbits_dict_by_id)

    def update_laser_distances(self, moving_objects_dict_by_id: Dict[id, MovingObject]) -> None:
        for moving_object in self.moving_objects:
            moving_object.update_laser_left_right(moving_objects_dict_by_id)

    @staticmethod
    def update_orbits(orbits_dict_by_id: Dict[id, Orbit], moving_objects_dict_by_id: Dict[id, MovingObject]) -> None:
        for orbit_id in orbits_dict_by_id.keys():
            orbits_dict_by_id[orbit_id].update_moving_object_positions()

        for orbit_id in orbits_dict_by_id.keys():
            orbits_dict_by_id[orbit_id].update_laser_connections(
                orbits_dict_by_id)
            orbits_dict_by_id[orbit_id].update_laser_distances(
                moving_objects_dict_by_id)
