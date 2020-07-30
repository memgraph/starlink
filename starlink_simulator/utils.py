import starlink_simulator.constants as const
import csv
import math as m


# Prints the coordinates of all the objects in the orbits
def print_orbits_and_objects(orbits):
    for i in orbits:
        for j in i.moving_objects:
            print("Orbit: ", i.id, "  Object: (", j.x, ", ", j.y, ")")


# Prints the indexes of all the laser connections of objects in the orbits
def print_laser_connections(orbits):
    for i in orbits:
        for j in i.moving_objects:
            print("Orbit: ", i.id, "  Object: ", j.id, " (", j.x, ", ", j.y, ")  Laser left: (", j.laser_left_id,
                  ")  Laser right: (", j.laser_right_id, ")  Laser up: (", j.laser_up_id, ")  Laser down: (", j.laser_down_id, ")")


# Prints all the cities
def print_cities(cities):
    for city in cities:
        print("City: ", city.name, "  Id: ", city.id,
              "  Position: (", city.x, ", ", city.y, ")")


# Calculates the distance between two points in 2D
def distance(point_a, point_b):
    return m.sqrt((point_b.y-point_a.y)**2 + (point_b.x-point_a.x)**2)


# Calculates the distance between two points in 3D
def distance3D(point_a, point_b):
    return m.sqrt((point_b.x - point_a.x)**2 + (point_b.y - point_a.y)**2 + (point_b.z - point_a.z)**2)


# Calculates the distance between two ECI points in 3D in KM
def eci_distance(point_a, point_b):
    return m.sqrt((point_a.eci_x - point_b.eci_x)**2 + (point_a.eci_y - point_b.eci_y)**2 + (point_a.eci_z - point_b.eci_z)**2)


# Calculates angle in between two objects
def calculate_angle(point_a, point_b):
    angle = m.acos(const.SAT_ALT / eci_distance(point_a, point_b))
    return angle
