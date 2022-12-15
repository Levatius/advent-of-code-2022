# https://adventofcode.com/2022/day/15

import numpy as np
import portion as p
import re
from dataclasses import dataclass, field


@dataclass
class Sensor:
    position: np.array
    beacon_position: np.array
    scan_distance: int = field(init=False)

    @classmethod
    def from_readout_str(cls, readout_str):
        readout_pattern = re.compile(
            r'Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): '
            r'closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)'
        )
        m = readout_pattern.match(readout_str)
        sensor_position = np.array((m['sensor_x'], m['sensor_y']), dtype=int)
        closest_beacon_position = np.array((m['beacon_x'], m['beacon_y']), dtype=int)
        return cls(sensor_position, closest_beacon_position)

    def __post_init__(self):
        self.scan_distance = int(np.linalg.norm(self.beacon_position - self.position, 1))

    def scan(self, y):
        sensor_x, sensor_y = self.position
        # These equations come from intersecting a diamond (L1 circle) with a horizontal line
        lower = sensor_x - self.scan_distance + abs(sensor_y - y)
        upper = sensor_x + self.scan_distance - abs(sensor_y - y)
        # Check fails if the scan area does not intersect the given horizontal line
        if lower <= upper:
            return p.closed(lower, upper)


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        sensors = [Sensor.from_readout_str(readout_str) for readout_str in f.read().splitlines()]
    return sensors


def run_part_1(sensors, y):
    # Get all scans with the given y value
    scans = (scan for sensor in sensors if (scan := sensor.scan(y)))
    combined_scan = p.Interval(*scans)

    # Find any sensors or beacons with the given y value
    sensors = (p.singleton(sensor.position[0]) for sensor in sensors if sensor.position[1] == y)
    unique_sensors = p.Interval(*sensors)
    beacons = (p.singleton(sensor.beacon_position[0]) for sensor in sensors if sensor.beacon_position[1] == y)
    unique_beacons = p.Interval(*beacons)

    # Remove any sensors or beacons from the scan
    unoccupied_scan = combined_scan - unique_sensors - unique_beacons
    print(f'Unoccupied Scan: {unoccupied_scan}')


def run_part_2(sensors, x_bounds, y_bounds):
    for y in range(y_bounds.lower, y_bounds.upper + 1):
        scans = (scan for sensor in sensors if (scan := sensor.scan(y)))
        combined_scan = p.Interval(*scans)
        if len(combined_scan) > 1:
            confined_scan = combined_scan & x_bounds
            distress_beacon_x = next(p.iterate(x_bounds - confined_scan, step=1))
            print(f'Distress Beacon: {distress_beacon_x, y}')
            break


def main():
    sensors = get_data()
    run_part_1(sensors, y=2000000)
    run_part_2(sensors, x_bounds=p.closed(0, 4000000), y_bounds=p.closed(0, 4000000))


if __name__ == '__main__':
    main()
