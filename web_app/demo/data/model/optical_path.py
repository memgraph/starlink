from __future__ import annotations
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import List, Any
from demo.data.model.city import City


@dataclass
class OpticalPath:
    city1: Any
    city2: Any
    transmission_time_ms: float

    @staticmethod
    def import_optical_paths(file_path: Path) -> List[OpticalPath]:
        paths = []
        with file_path.open() as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                optical_path = OpticalPath(
                    city1=row["Source"],
                    city2=row["Destination"],
                    transmission_time_ms=row["Latency"])
                paths.append(optical_path)
        return paths
