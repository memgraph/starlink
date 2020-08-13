import math as m


def distance(point_a, point_b):
    return m.sqrt((point_b.y-point_a.y)**2 + (point_b.x-point_a.x)**2)


def eci_distance(point_a, point_b):
    return m.sqrt((point_a.eci_x - point_b.eci_x)**2 + (point_a.eci_y - point_b.eci_y)**2 + (point_a.eci_z - point_b.eci_z)**2)

