

class StationaryObject:
    def __init__(self, id, x, y, z, eci_x_positions, eci_y_positions, eci_z_positions):
        self.id = id

        self.x = x
        self.y = y
        self.z = z

        self.current_position = 0
        self.positions_lenght = len(eci_x_positions)

        self.eci_x_positions = eci_x_positions
        self.eci_y_positions = eci_y_positions
        self.eci_z_positions = eci_z_positions

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]

    def update_position(self):
        self.current_position += 1
        if self.current_position == self.positions_lenght:
            self.current_position = 0

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]
