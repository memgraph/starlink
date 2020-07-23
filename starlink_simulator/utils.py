import csv
import math as m
from starlink_simulator.city import City as City

# Imports city coordinates from a specified .csv file
def import_cities(path):
    cities = []
    with open(path,'r') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            city = City(id=row[0], x=row[1], y=row[2], z=row[3], name=row[4])
            cities.append(city)
    return cities

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

# Computes the distance between two points in 2D
def distance(point_a, point_b):
    return m.sqrt((point_b.y-point_a.y)**2 + (point_b.x-point_a.x)**2)

# Computes the distance between two points in 3D
def distance3D(point_a, point_b):
    return m.sqrt((point_b.x - point_a.x)**2 + (point_b.y - point_a.y)**2 + (point_b.z - point_a.z)**2)

#Calculates angle in between two objects
def calculate_angle(object_a, object_b):
    '''
    angle = m.acos( (object_a.x*object_b.x + object_a.y*object_b.y + object_a.z*object_b.z) 
    / ( m.sqrt((object_a.x**2 + object_a.y**2 + object_a.z**2) * (object_b.x**2 + object_b.y**2 + object_b.z**2)) ))
    return angle
    '''

    angle = m.acos( 1500 / distance3D(object_a, object_b) )
    return angle