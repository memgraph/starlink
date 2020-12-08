from dataclasses import dataclass


@dataclass
class Relationship:
    xS: float
    yS: float

    xE: float
    yE: float

    transmission_time: float
