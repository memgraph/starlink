import collections
import os
import logging
from pathlib import Path
from simulator.models import City, MovingObject, Orbit
from skyfield.api import EarthSatellite
from typing import List, Dict, Any


logger = logging.getLogger('simulator')

ORBIT_ENDS_CONNECTED = bool(os.getenv('ORBIT_ENDS_CONNECTED', 'false'))

OrbitsAndObjects = collections.namedtuple(
    'ObjectsAndOrbits', ['orbits_dict_by_id',
                         'moving_objects_dict_by_id'])


def read_tle(file_path: Path) -> None:
    satellites = []
    logger.info(f'Reading TLE from file path {file_path}...')
    with file_path.open() as f:
        lines = f.readlines()

    cnt = 0
    tmp = lines[cnt].strip().split(',')
    num_of_orbits = int(tmp[0].strip().split('=')[1])
    num_objects_in_orbit = int(tmp[1].strip().split('=')[1])

    num_of_all_objects = num_of_orbits * num_objects_in_orbit
    cnt += 1
    while(cnt < num_of_all_objects * 3 + 1):
        line1 = lines[cnt+1]
        line2 = lines[cnt+2]
        satellites.append(EarthSatellite(line1, line2))
        cnt += 3
    return num_of_orbits, num_objects_in_orbit, satellites


def generate_orbits_and_moving_objects(file_path: Path, time: Any) -> OrbitsAndObjects:
    num_of_orbits, num_objects_in_orbit, satellites = read_tle(file_path)

    object_data = []
    for satellite in satellites:
        geocentric = satellite.at(time)
        subpoint = geocentric.subpoint()
        position_gcrs = geocentric.position.km
        object_data.append([subpoint, position_gcrs])

    orbits_dict_by_id = {}
    moving_objects_dict_by_id = {}

    object_id = 0
    for orbit_id in range(num_of_orbits):
        orbit = Orbit(orbit_id)
        for id_in_orbit in range(num_objects_in_orbit):
            if id_in_orbit == 0:
                if(object_id == 0 and ORBIT_ENDS_CONNECTED):
                    laser_left_id = num_of_orbits * num_objects_in_orbit - 1
                elif(object_id == 0 and not ORBIT_ENDS_CONNECTED):
                    laser_left_id = -1
                else:
                    laser_left_id = num_objects_in_orbit * orbit_id - 1
                laser_left_id_in_orbit = num_objects_in_orbit - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = id_in_orbit + 1
            elif id_in_orbit == num_objects_in_orbit - 1:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = id_in_orbit - 1
                if(object_id == num_of_orbits*num_objects_in_orbit-1 and ORBIT_ENDS_CONNECTED):
                    laser_right_id = 0
                elif(object_id == num_of_orbits*num_objects_in_orbit-1 and  not ORBIT_ENDS_CONNECTED):
                    laser_right_id = -1
                else:
                    laser_right_id = num_objects_in_orbit * orbit_id + num_objects_in_orbit
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = id_in_orbit - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = id_in_orbit + 1

            imo = MovingObject(id=object_id,
                               id_in_orbit=id_in_orbit,
                               orbit_id=orbit_id,
                               num_of_orbits=num_of_orbits,
                               latitude_positions=object_data[object_id][0].latitude.degrees,
                               longitude_positions=object_data[object_id][0].longitude.degrees,
                               elevation_positions=object_data[object_id][0].elevation.km,
                               eci_x_positions=object_data[object_id][1][0],
                               eci_y_positions=object_data[object_id][1][1],
                               eci_z_positions=object_data[object_id][1][2],
                               laser_left_id=laser_left_id,
                               laser_left_id_in_orbit=laser_left_id_in_orbit,
                               laser_right_id=laser_right_id,
                               laser_right_id_in_orbit=laser_right_id_in_orbit)

            moving_objects_dict_by_id[object_id] = imo
            orbit.add_object(imo)
            object_id += 1
        orbits_dict_by_id[orbit_id] = orbit
    return OrbitsAndObjects(orbits_dict_by_id, moving_objects_dict_by_id)
