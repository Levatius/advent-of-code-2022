# https://adventofcode.com/2022/day/18

import networkx as nx
import numpy as np

from structures import Cube


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        cubes = [Cube(np.array(position_str.split(','), dtype=int)) for position_str in f.read().splitlines()]
    return cubes


def run_part_1(cubes):
    exposed_sides = set()
    for cube in cubes:
        for side in cube.sides:
            if side in exposed_sides:
                exposed_sides.remove(side)
            else:
                exposed_sides.add(side)
    print(f'Exposed Sides: {len(exposed_sides)}')
    return exposed_sides


def run_part_2(exposed_sides):
    graph = nx.Graph()
    exposed_positions = [tuple(side.position) for side in exposed_sides]
    for side in exposed_sides:
        for connected_position in side.get_connected_exposed_sides(exposed_positions):
            graph.add_edge(tuple(side.position), connected_position)
    largest_connected_component = max(nx.connected_components(graph), key=len)
    print(f'Exterior Sides: {len(largest_connected_component)}')


def main():
    cubes = get_data()
    exposed_sides = run_part_1(cubes)
    run_part_2(exposed_sides)


if __name__ == '__main__':
    main()
