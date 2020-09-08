import csv
import demo.data.constants as const
from demo.data.model.optical_path import OpticalPath


def import_optical_paths():
    paths = []
    with open(const.OPTICAL_FILE, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            optical_path = OpticalPath(row["Source"], row["Destination"], row["Latency"])
            paths.append(optical_path)
    return paths
