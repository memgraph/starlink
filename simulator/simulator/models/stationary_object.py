from dataclasses import dataclass
from typing import List


@dataclass
class StationaryObject:
    id: int
    x: float
    y: float
    z: float
    eci_x_positions: List
    eci_y_positions: List
    eci_z_positions: List

    def __post_init__(self):
        self.current_position = 0
        self.positions_lenght = len(self.eci_x_positions)

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]

    def update_position(self) -> None:
        self.current_position += 1
        if self.current_position == self.positions_lenght:
            self.current_position = 0

        self.eci_x = self.eci_x_positions[self.current_position]
        self.eci_y = self.eci_y_positions[self.current_position]
        self.eci_z = self.eci_z_positions[self.current_position]
