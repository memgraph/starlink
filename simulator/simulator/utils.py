import math


def eci_distance(point_a, point_b):
    return math.sqrt((point_a.eci_x - point_b.eci_x)**2 + (point_a.eci_y - point_b.eci_y)**2 + (point_a.eci_z - point_b.eci_z)**2)
