# https://adventofcode.com/2022/day/9

import numpy as np
from dataclasses import dataclass, field
from more_itertools import windowed


@dataclass
class Movement:
    DIRECTIONS_MAP = {'L': np.array([-1, 0]), 'R': np.array([1, 0]), 'U': np.array([0, 1]), 'D': np.array([0, -1])}
    direction: np.array
    steps: int

    @classmethod
    def from_movement_str(cls, movement_str):
        direction_str, steps_str = movement_str.split(' ')
        return cls(cls.DIRECTIONS_MAP[direction_str], int(steps_str))


@dataclass
class Knot:
    pos: np.array = field(default_factory=lambda: np.zeros(2))

    def move(self, direction):
        self.pos += direction


class Rope:
    def __init__(self, length=2):
        self.knots = [Knot() for _ in range(length)]
        self.tail_pos_log = set()
        self.log_tail_pos()

    @property
    def head(self):
        return self.knots[0]

    @property
    def tail(self):
        return self.knots[-1]

    @staticmethod
    def distance(knot_a, knot_b):
        return np.linalg.norm(knot_a.pos - knot_b.pos)

    def is_stable(self, knot_a, knot_b):
        # Two knots are considered stable if they are adjacent or diagonal to each other
        return self.distance(knot_a, knot_b) <= 2 ** 0.5

    @staticmethod
    def get_stabilising_direction(leading_knot, tailing_knot):
        # Example: If leading knot is at (2,1) and tailing knot is at (0,0), stabilising direction = (1,1)
        return np.fromiter(map(np.sign, leading_knot.pos - tailing_knot.pos), dtype=int)

    def move(self, direction):
        self.head.move(direction)
        for leading_knot, tailing_knot in windowed(self.knots, n=2, step=1):
            # Do not move the tailing knot if it is stable with the leading knot
            if self.is_stable(leading_knot, tailing_knot):
                continue
            stabilising_direction = self.get_stabilising_direction(leading_knot, tailing_knot)
            tailing_knot.move(stabilising_direction)
        self.log_tail_pos()

    def log_tail_pos(self):
        self.tail_pos_log.add(tuple(self.tail.pos))


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        movements = list(map(Movement.from_movement_str, f.read().splitlines()))
    return movements


def run(rope, movements):
    for movement in movements:
        for _ in range(movement.steps):
            rope.move(movement.direction)
    print(f'Positions Visited: {len(rope.tail_pos_log)}')


def main():
    movements = get_data()
    run(Rope(), movements)
    run(Rope(length=10), movements)


if __name__ == '__main__':
    main()
