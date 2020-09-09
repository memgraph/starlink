from dataclasses import dataclass


@dataclass
class Relationship:
    xS: float
    yS: float
    zS: float

    xE: float
    yE: float
    zE: float

    transmission_time: float
