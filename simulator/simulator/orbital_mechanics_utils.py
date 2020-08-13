from simulator.constants import NUM_OBJ, NUM_ORB
from simulator.models import City
from simulator.models import MovingObject
from simulator.models import Orbit
from skyfield.api import EarthSatellite
import collections
from pathlib import Path


OrbitsAndObjects = collections.namedtuple(
    'ObjectsAndOrbits', ['orbits_dict_by_id', 'moving_objects_dict_by_id'])


def read_tle(file_path):
    satellites = []
    path = Path(__file__).parent.parent / file_path
    with path.open() as f:
        lines = f.readlines()
    cnt = 0
    while(cnt < len(lines)):
        line1 = lines[cnt+1]
        line2 = lines[cnt+2]

        satellites.append(EarthSatellite(line1, line2))
        cnt += 3
    return satellites


def generate_orbits_and_moving_objects(file_path, time):
    satellites = read_tle(file_path)

    object_data = []
    for satellite in satellites:
        geocentric = satellite.at(time)
        subpoint = geocentric.subpoint()
        position_gcrs = geocentric.position.km
        object_data.append([subpoint, position_gcrs])

    orbits_dict_by_id = {}
    moving_objects_dict_by_id = {}

    object_id = 0
    for orbit_id in range(NUM_ORB):
        orbit = Orbit(orbit_id)
        for id_in_orbit in range(NUM_OBJ):
            if id_in_orbit == 0:
                laser_left_id = NUM_OBJ * orbit_id + NUM_OBJ - 1
                laser_left_id_in_orbit = NUM_OBJ - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = id_in_orbit + 1
            elif id_in_orbit == NUM_OBJ - 1:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = id_in_orbit - 1
                laser_right_id = NUM_OBJ * orbit_id
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = id_in_orbit - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = id_in_orbit + 1

            imo = MovingObject(id=object_id,
                               id_in_orbit=id_in_orbit,
                               orbit_id=orbit_id,
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
