from __future__ import annotations
import csv
from pathlib import Path
from typing import List


class OpticalPath():
    def __init__(self, city1, city2, transmission_time_ms):
        self.city1 = city1
        self.city2 = city2
        self.transmission_time_ms = transmission_time_ms

    @staticmethod
    def import_optical_paths(file_path: Path) -> List[OpticalPath]:
        paths = []
        with file_path.open() as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                optical_path = OpticalPath(
                    row["Source"], row["Destination"], row["Latency"])
                paths.append(optical_path)
        return paths
