# https://adventofcode.com/2022/day/15

import numpy as np
import portion as p
import re
from dataclasses import dataclass, field


@dataclass
class Sensor:
    position: np.array
    closest_beacon_position: np.array
    scan_distance: int = field(init=False)

    @classmethod
    def from_readout_str(cls, readout_str):
        readout_pattern = re.compile(
            r'Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): '
            r'closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)'
        )
        m = readout_pattern.match(readout_str)
        sensor_position = np.array((int(m['sensor_x']), int(m['sensor_y'])))
        closest_beacon_position = np.array((int(m['beacon_x']), int(m['beacon_y'])))
        return cls(sensor_position, closest_beacon_position)

    def __post_init__(self):
        self.scan_distance = int(np.linalg.norm(self.closest_beacon_position - self.position, 1))

    def get_scan_row(self, y):
        # Part 1 Example: y=10 would give us lower=-2, upper=24
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
    scan_rows = (scan_row for sensor in sensors if (scan_row := sensor.get_scan_row(y)))
    combined_scan_row = p.Interval(*scan_rows)
    sensors_on_scan_row = (p.singleton(sensor.position[0]) for sensor in sensors
                           if sensor.position[1] == y)
    beacons_on_scan_row = (p.singleton(sensor.closest_beacon_position[0]) for sensor in sensors
                           if sensor.closest_beacon_position[1] == y)
    unoccupied_scan_row = combined_scan_row - p.Interval(*beacons_on_scan_row) - p.Interval(*sensors_on_scan_row)
    print(f'Unoccupied Scan Row: {unoccupied_scan_row}')


def run_part_2(sensors, x_space, y_space):
    for y in range(y_space.upper):
        scan_rows = [scan_row for sensor in sensors if (scan_row := sensor.get_scan_row(y))]
        combined_scan_row = p.Interval(*scan_rows)
        if len(combined_scan_row) > 1:
            confined_scan_row = combined_scan_row & x_space
            distress_beacon_x = next(p.iterate(x_space - confined_scan_row, step=1))
            print(f'Distress Beacon: {distress_beacon_x, y}')
            break


def main():
    sensors = get_data()
    run_part_1(sensors, y=2000000)
    run_part_2(sensors, x_space=p.closed(0, 4000000), y_space=p.closed(0, 4000000))


if __name__ == '__main__':
    main()
