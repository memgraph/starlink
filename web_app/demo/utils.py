import csv
import demo.data.constants as const
from demo.data.model.optical_path import OpticalPath


"""TODO: remove before deployment"""
"""
import math as m


old_sats = []


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def distance_coordinates(new_sats):
    cnt = 0
    if(old_sats != []):
        for i in range(len(new_sats)):
            diff = m.sqrt((new_sats[i].x-old_sats[i].x)
                          ** 2 + (new_sats[i].y-old_sats[i].y)**2)
            if diff == 0:
                cnt += 1
        print("CNT: ", cnt)
"""

'''
def import_optical_paths():
    paths = []
    with open(const.OPTICAL_FILE, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row:
                optical_path = OpticalPath(city1=row[0], city2=row[1], transmission_time_ms=row[2])
                paths.append(optical_path)
    return paths
'''

def import_optical_paths():
    paths = []
    with open(const.OPTICAL_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            optical_path = OpticalPath(row["Source"], row["Destination"], row["Latency"])
            paths.append(optical_path)
    return paths
