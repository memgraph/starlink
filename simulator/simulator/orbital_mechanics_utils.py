from simulator.constants import NUM_OBJ, NUM_ORB, SAT_ALT
from simulator.models import City
from simulator.models import MovingObject
from simulator.models import Orbit
from skyfield.api import EarthSatellite
import collections

OrbitsAndObjects = collections.namedtuple(
    'ObjectsAndOrbits', ['orbits_dict_by_id', 'moving_objects_dict_by_id'])


def read_tle(file_path):
    satellites = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    cnt = 0
    while(cnt < len(lines)):
        line1 = lines[cnt+1]
        line2 = lines[cnt+2]

        satellites.append(EarthSatellite(line1, line2))
        cnt += 3
    return satellites


def generate_moving_objects(file_path, time):
    satellites = read_tle(file_path)

    object_data = []
    for satellite in satellites:
        geocentric = satellite.at(time)
        subpoint = geocentric.subpoint()
        position_gcrs = geocentric.position.km
        object_data.append([subpoint, position_gcrs])

    orbits_dict_by_id = {}
    moving_objects_dict_by_id = {}

    orbit_id = 0
    object_id = 0
    for x in range(NUM_ORB):
        orbit = Orbit(orbit_id)
        for y in range(NUM_OBJ):
            if y == 0:
                laser_left_id = NUM_OBJ * x + NUM_OBJ - 1
                laser_left_id_in_orbit = NUM_OBJ - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = y + 1
            elif y == NUM_OBJ - 1:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = y - 1
                laser_right_id = NUM_OBJ * x
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = y - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = y + 1
            imo = MovingObject(object_id, y, orbit_id, object_data[object_id][0].latitude.degrees,
                               object_data[object_id][0].longitude.degrees, SAT_ALT, object_data[object_id][1][0], object_data[object_id][1][1], object_data[object_id][1][2], laser_left_id, laser_left_id_in_orbit, laser_right_id, laser_right_id_in_orbit)
            moving_objects_dict_by_id[object_id] = imo
            orbit.add_object(imo)
            object_id += 1
        orbits_dict_by_id[orbit_id] = orbit
        orbit_id += 1
    return OrbitsAndObjects(orbits_dict_by_id, moving_objects_dict_by_id)
