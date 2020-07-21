
class Orbit:
    def __init__(self, id, horiz_ver_id, is_horizontal, starting_point, ending_point, number_of_objects, moving_object_speed):
        self.id = id
        self.horiz_ver_id = horiz_ver_id
        self.is_horizontal = is_horizontal
        self.starting_point = starting_point
        self.ending_point = ending_point
        self.number_of_objects = number_of_objects
        self.moving_object_speed = moving_object_speed
        self.moving_objects = []

    def add_object(self, moving_objects):
        self.moving_objects.append(moving_objects)

    def update_moving_object_positions(self):
        for moving_object in self.moving_objects:
            if self.is_horizontal:
                moving_object.x += self.moving_object_speed
                if moving_object.x == self.ending_point + 1:
                    moving_object.x = self.starting_point
            else:
                moving_object.y += self.moving_object_speed
                if moving_object.y == self.ending_point + 1:
                    moving_object.y = self.starting_point

    def update_laser_connections(self, orbits, num_of_orbits_horizontal, num_of_orbits_vertical):
        for moving_object in self.moving_objects:
            moving_object.update_laser_up(orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
            moving_object.update_laser_down(orbits, num_of_orbits_horizontal, num_of_orbits_vertical)
