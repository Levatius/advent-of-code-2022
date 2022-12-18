import numpy as np
from dataclasses import dataclass, field


@dataclass
class Shape:
    position: np.array
    local_rock_positions: list[np.array]

    @property
    def rock_positions(self):
        return (self.position + local_rock_position for local_rock_position in self.local_rock_positions)


@dataclass
class HLine(Shape):
    local_rock_positions: list[np.array] = field(
        default_factory=lambda: list(map(np.array, [(0, 0), (1, 0), (2, 0), (3, 0)])))


@dataclass
class Plus(Shape):
    local_rock_positions: list[np.array] = field(
        default_factory=lambda: list(map(np.array, [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)])))


@dataclass
class L(Shape):
    local_rock_positions: list[np.array] = field(
        default_factory=lambda: list(map(np.array, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])))


@dataclass
class VLine(Shape):
    local_rock_positions: list[np.array] = field(
        default_factory=lambda: list(map(np.array, [(0, 0), (0, 1), (0, 2), (0, 3)])))


@dataclass
class Square(Shape):
    local_rock_positions: list[np.array] = field(
        default_factory=lambda: list(map(np.array, [(0, 0), (1, 0), (0, 1), (1, 1)])))
