import starlink_simulator.constants as const
import math as m


# Calculates the distance between two points in 2D
def distance(point_a, point_b):
    return m.sqrt((point_b.y-point_a.y)**2 + (point_b.x-point_a.x)**2)


# Calculates the distance between two ECI points in 3D in KM
def eci_distance(point_a, point_b):
    return m.sqrt((point_a.eci_x - point_b.eci_x)**2 + (point_a.eci_y - point_b.eci_y)**2 + (point_a.eci_z - point_b.eci_z)**2)


# Calculates angle in between two objects
def calculate_angle(point_a, point_b):
    angle = m.acos(const.SAT_ALT / eci_distance(point_a, point_b)) * 180.0/m.pi
    return angle


"""TODO: remove before deployment"""
"""
def eci_distance_coordinates(eci_x_a, eci_y_a, eci_z_a, eci_x_b, eci_y_b, eci_z_b):
    return m.sqrt((eci_x_a - eci_x_b)**2 + (eci_y_a - eci_y_b)**2 + (eci_z_a - eci_z_b)**2)


def distance_coordinates(x_a, y_a, x_b, y_b):
    return m.sqrt((x_a-x_b)**2 + (y_a-y_b)**2)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
"""
