import csv
import math as m
from city import City as City


def import_cities(path):
    cities = []
    with open(path,'r') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            city = City(id=row[0], x=row[1], y=row[2], z=row[3], name=row[4])
            cities.append(city)
    return cities

# prints the coordinates of all the objects in the orbits
def print_orbits_and_objects(orbits):
    for i in orbits:
        for j in i.moving_objects:
            print("Orbit: ", i.id, "  Object: (", j.x, ", ", j.y, ")")

# prints the indexes of all the laser connections of objects in the orbits
def print_laser_connections(orbits):
    for i in orbits:
        for j in i.moving_objects:
            print("Orbit: ", i.id, "  Object: ", j.id, " (", j.x, ", ", j.y, ")  Laser left: (", j.laser_left_id,
                  ")  Laser right: (", j.laser_right_id, ")  Laser up: (", j.laser_up_id, ")  Laser down: (", j.laser_down_id, ")")

# prints all the imported cities
def print_cities(cities):
    for city in cities:
        print("City: ", city.name, "  Id: ", city.id,
              "  Position: (", city.x, ", ", city.y, ")")


def distance(point_a, point_b):
    return m.sqrt((point_a.y-point_b.y)**2 + (point_a.x-point_b.x)**2)