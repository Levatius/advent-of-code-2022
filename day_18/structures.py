import numpy as np
from dataclasses import dataclass, field

ALL_OFFSETS = list(map(np.array, [(-0.5, 0, 0), (0.5, 0, 0), (0, -0.5, 0), (0, 0.5, 0), (0, 0, -0.5), (0, 0, 0.5)]))


@dataclass
class Cube:
    position: np.array

    @staticmethod
    def get_side_offsets():
        yield from ALL_OFFSETS

    @property
    def sides(self):
        # Every cube has 6 sides
        return (Side.from_cube(self, side_offset) for side_offset in self.get_side_offsets())


@dataclass
class Side:
    position: np.array
    direction_from_cube: np.array = field(default_factory=lambda: np.array((0, 0)))

    @classmethod
    def from_cube(cls, cube, offset):
        position = cube.position + offset
        return cls(position, direction_from_cube=offset)

    @property
    def plane_index(self):
        # Example: Sides parallel to the y-plane have plane index 1
        return next(i for i, value in enumerate(self.direction_from_cube) if value != 0)

    def get_edge_offsets(self):
        # Example: Sides parallel to the y-plane only need the 4 offsets in the x and z directions
        yield from (offset for offset in ALL_OFFSETS if offset[self.plane_index] == 0)

    @property
    def edges(self):
        # Every side has 4 edges
        return (Edge.from_side(self, edge_offset) for edge_offset in self.get_edge_offsets())

    def get_connected_exposed_sides(self, exposed_positions):
        for edge in self.edges:
            adjacent_side_positions = edge.get_adjacent_side_positions()
            # Reduce our adjacent side positions to only the ones we want
            adjacent_exposed_positions = []
            for position in adjacent_side_positions:
                # Skip adjacent sides that are not exposed (or this side)
                is_not_exposed = position not in exposed_positions
                is_self = position == tuple(self.position)
                if is_not_exposed or is_self:
                    continue
                adjacent_exposed_positions.append(position)

            if len(adjacent_exposed_positions) == 3:
                # Side is "connected" to 3 other sides through their shared edge
                # We use side.direction_from_cube to determine the correct side to connect to
                for position in adjacent_exposed_positions:
                    i = self.plane_index
                    if position[i] == self.position[i] + self.direction_from_cube[i]:
                        yield position
                        break
            else:
                yield from adjacent_exposed_positions

    def __eq__(self, other):
        return np.array_equal(self.position, other.position)

    def __hash__(self):
        return hash(tuple(self.position))


@dataclass
class Edge:
    position: np.array
    direction_from_cube: np.array
    direction_from_side: np.array

    @classmethod
    def from_side(cls, side, offset):
        position = side.position + offset
        return cls(position, direction_from_cube=side.direction_from_cube, direction_from_side=offset)

    @property
    def axis_index(self):
        # Example: Edges parallel to the y-axis have axis index 1
        return next(i for i, value in enumerate(self.direction_from_cube + self.direction_from_side) if value == 0)

    def get_adjacent_side_offsets(self):
        # Example: Edges parallel to the y-plane only need the 4 offsets in the x and z directions
        yield from (offset for offset in ALL_OFFSETS if offset[self.axis_index] == 0)

    def get_adjacent_side_positions(self):
        return [tuple(self.position + offset) for offset in self.get_adjacent_side_offsets()]
