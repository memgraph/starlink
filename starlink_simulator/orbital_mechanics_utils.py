import starlink_simulator.constants as const
import csv
import numpy as np
from starlink_simulator.city import City
from starlink_simulator.moving_object import MovingObject
from starlink_simulator.orbit import Orbit
from skyfield.api import load, EarthSatellite, Topos


satellites = []
ts = load.timescale(builtin=True)
minutes = np.arange(0, 24*60, 1)
time = ts.utc(2020, 7, 29, 0, minutes)


def readTLE():
    with open(const.TLE_FILE, 'r') as f:
        lines = f.readlines()
    cnt = 0
    while(cnt < len(lines)):
        line1 = lines[cnt+1]
        line2 = lines[cnt+2]

        sat = EarthSatellite(line1, line2)
        satellites.append(sat)
        cnt += 3


# Imports city coordinates from a specified .csv file
def import_cities():
    cities = []
    with open(const.CITIES_FILE, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            topos = Topos(latitude_degrees=float(row[1]), longitude_degrees=float(
                row[2]), elevation_m=float(row[3]))
            geocentric = topos.at(time)
            city = City(id=row[0], x=topos.latitude.degrees, y=topos.longitude.degrees, z=topos.elevation.km,
                        eci_x_positions=geocentric.position.km[0], eci_y_positions=geocentric.position.km[1], eci_z_positions=geocentric.position.km[2], name=row[4])
            cities.append(city)
    return cities


def generateMovingObjects():

    readTLE()

    object_data = []
    for sat in satellites:
        geocentric = sat.at(time)
        subpoint = geocentric.subpoint()
        position_gcrs = geocentric.position.km
        object_data.append([subpoint, position_gcrs])

    orbits = []
    orbits_dict = {}
    moving_objects = []
    moving_objects_dict = {}

    orbit_id = 0
    object_id = 0
    for x in range(const.NUM_ORB):
        orbit = Orbit(orbit_id)
        for y in range(const.NUM_OBJ):
            if y == 0:
                laser_left_id = const.NUM_OBJ * x + const.NUM_OBJ - 1
                laser_left_id_in_orbit = const.NUM_OBJ - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = y + 1
            elif y == const.NUM_OBJ - 1:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = y - 1
                laser_right_id = const.NUM_OBJ * x
                laser_right_id_in_orbit = 0
            else:
                laser_left_id = object_id - 1
                laser_left_id_in_orbit = y - 1
                laser_right_id = object_id + 1
                laser_right_id_in_orbit = y + 1
            imo = MovingObject(object_id, y, orbit_id, object_data[object_id][0].longitude.degrees,
                               object_data[object_id][0].latitude.degrees, const.SAT_ALT, object_data[object_id][1][0], object_data[object_id][1][1], object_data[object_id][1][2], laser_left_id, laser_left_id_in_orbit, laser_right_id, laser_right_id_in_orbit)
            moving_objects.append(imo)
            moving_objects_dict[object_id] = imo
            orbit.add_object(imo)
            object_id += 1
        orbits.append(orbit)
        orbits_dict[orbit_id] = orbit
        orbit_id += 1
    return orbits, orbits_dict, moving_objects, moving_objects_dict
