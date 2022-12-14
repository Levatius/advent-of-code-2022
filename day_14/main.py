# https://adventofcode.com/2022/day/14

import numpy as np
from dataclasses import dataclass, field
from more_itertools import windowed


@dataclass
class Sand:
    position: np.array
    FALL_OFFSETS = [(0, 1), (-1, 1), (1, 1)]

    def fall(self, cave):
        for fall_offset in self.FALL_OFFSETS:
            fall_position = self.position + np.array(fall_offset)
            if not cave.check_for_collision(fall_position):
                self.position = fall_position
                return True
        return False


@dataclass
class SandSpawner:
    position: np.array = field(default_factory=lambda: np.array((500, 0)))

    def spawn(self):
        return Sand(self.position)


@dataclass
class RockPath:
    start: np.array
    end: np.array
    rocks: np.ndarray = field(init=False)

    @property
    def length(self):
        return int(np.linalg.norm(self.end - self.start))

    def __post_init__(self):
        self.rocks = np.linspace(self.start, self.end, num=self.length + 1, dtype=int)


@dataclass
class RockStructure:
    rock_paths: list[RockPath]

    @classmethod
    def from_rock_structure_str(cls, rock_structure_str):
        rock_path_points = (np.array(point_str.split(','), dtype=int) for point_str in rock_structure_str.split(' -> '))
        rock_paths = [RockPath(start, end) for start, end in windowed(rock_path_points, n=2, step=1)]
        return cls(rock_paths)

    @property
    def rocks(self):
        return (rock_path.rocks for rock_path in self.rock_paths)


@dataclass
class Cave:
    objects_at_rest: set
    floor_exists: bool
    sand_spawner: SandSpawner = field(default_factory=SandSpawner)
    sand_at_rest_total: int = 0
    floor_level: int = field(init=False)

    @classmethod
    def from_rock_structure_data(cls, rock_structure_data, floor_exists=False):
        objects_at_rest = set()
        rock_structures = map(RockStructure.from_rock_structure_str, rock_structure_data)
        for rock_structure in rock_structures:
            for rock_path in rock_structure.rock_paths:
                for rock in rock_path.rocks:
                    objects_at_rest.add(tuple(rock))
        return cls(objects_at_rest, floor_exists)

    def __post_init__(self):
        self.floor_level = max((y for x, y in self.objects_at_rest)) + 2

    def is_floor_level(self, position):
        return position[1] == self.floor_level

    def check_for_collision(self, position):
        collision_with_object_at_rest = tuple(position) in self.objects_at_rest
        collision_with_cave_floor = self.floor_exists and self.is_floor_level(position)
        return collision_with_object_at_rest or collision_with_cave_floor

    def simulate(self):
        sand = self.sand_spawner.spawn()
        # Treat floor level as the abyss line
        while not self.is_floor_level(sand.position):
            sand_in_motion = sand.fall(self)
            if not sand_in_motion:
                self.objects_at_rest.add(tuple(sand.position))
                self.sand_at_rest_total += 1
                # Stop if sand is blocking the spawner
                if np.array_equal(sand.position, self.sand_spawner.position):
                    break
                sand = self.sand_spawner.spawn()


def get_data(file_name='input.txt', floor_exists=False):
    with open(file_name) as f:
        cave = Cave.from_rock_structure_data(f.read().splitlines(), floor_exists)
    return cave


def run(cave):
    cave.simulate()
    print(f'Total Sand: {cave.sand_at_rest_total}')


def main():
    cave = get_data()
    run(cave)
    cave = get_data(floor_exists=True)
    run(cave)


if __name__ == '__main__':
    main()
