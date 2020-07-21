import csv
from city import City as City


def import_cities(path):
    cities = []
    with open(path,'r') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            city = City(id=row[0], x=row[1], y=row[2], z=row[3], name=row[4])
            cities.append(city)
    return cities