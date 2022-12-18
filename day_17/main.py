# https://adventofcode.com/2022/day/17

import numpy as np
from dataclasses import dataclass, field

from shapes import HLine, Plus, L, VLine, Square


@dataclass
class RockColumn:
    jet_directions: list[np.array]
    wall_bounds: tuple = (0, 8)
    shape_spawn_order: list = field(default_factory=lambda: [HLine, Plus, L, VLine, Square])
    fixed_rock_positions: set = field(init=False)

    def __post_init__(self):
        self.fixed_rock_positions = set((x, 0) for x in range(self.wall_bounds[1]))

    @property
    def total_height(self):
        return max((y for x, y in self.fixed_rock_positions), default=0)

    def get_jet_directions_iter(self):
        while True:
            for jet_direction in self.jet_directions:
                yield jet_direction

    def spawn_shapes(self, total, offset=np.array((2, 3))):
        count = 0
        while count < total:
            for shape_class in self.shape_spawn_order:
                spawn_position = np.array((0, self.total_height)) + np.array((1, 1)) + offset
                count += 1
                yield shape_class(spawn_position)
                if count == total:
                    break

    def move_shape(self, shape, direction):
        shape.position += direction
        if self.check_for_collision(shape):
            shape.position -= direction
            return False
        return True

    def check_for_collision(self, shape):
        for rock_position in shape.rock_positions:
            if tuple(rock_position) in self.fixed_rock_positions or rock_position[0] in self.wall_bounds:
                return True
        return False

    def simulate(self, total):
        jet_directions_iter = self.get_jet_directions_iter()
        for falling_shape in self.spawn_shapes(total):
            drop_successful = True
            while drop_successful:
                self.move_shape(falling_shape, direction=next(jet_directions_iter))
                drop_successful = self.move_shape(falling_shape, direction=np.array((0, -1)))

            for rock_position in falling_shape.rock_positions:
                self.fixed_rock_positions.add(tuple(rock_position))


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        jet_symbol_map = {'<': np.array((-1, 0)), '>': np.array((1, 0))}
        jet_directions = [jet_symbol_map[jet_symbol] for jet_symbol in f.read().strip()]
    return RockColumn(jet_directions)


def run(rock_column, rocks_total):
    rock_column.simulate(rocks_total)
    print(f'Total Height: {rock_column.total_height}')


def main():
    rock_column = get_data()
    run(rock_column, rocks_total=2022)
    # Part 2: Just determined the formula by inspection, not interesting enough to justify ruining the code for


if __name__ == '__main__':
    main()
