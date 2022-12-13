# https://adventofcode.com/2022/day/12

import networkx as nx
import numpy as np
from more_itertools import windowed

SPECIAL_ELEVATIONS = {'S': 'a', 'E': 'z'}


def convert_to_height(elevation):
    elevation = SPECIAL_ELEVATIONS[elevation] if elevation in SPECIAL_ELEVATIONS else elevation
    return ord(elevation)


def add_edges_from_array_lines(graph, array, transpose):
    array = array.T if transpose else array
    for k, line in enumerate(array):
        for (i, elevation_i), (j, elevation_j) in windowed(enumerate(line), n=2, step=1):
            # Node IDs need to be unique and correctly formatted when transposed
            node_i_id = (k, i) if transpose else (i, k)
            node_j_id = (k, j) if transpose else (j, k)

            # Convert elevation (str) to height (int)
            height_i = convert_to_height(elevation_i)
            height_j = convert_to_height(elevation_j)

            # Add an edge from [i] to [j] if climbable or is equal/lower
            if height_i >= height_j - 1:
                graph.add_edge(node_i_id, node_j_id)
            # Add an edge from [j] to [i] if climbable or is equal/lower
            if height_j >= height_i - 1:
                graph.add_edge(node_j_id, node_i_id)

            # Add elevation data to both nodes for referencing later
            graph.nodes[node_i_id]['elevation'] = elevation_i
            graph.nodes[node_j_id]['elevation'] = elevation_j


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        array = np.array([list(row) for row in f.read().splitlines()], str)
    graph = nx.MultiDiGraph()
    # Add edges between row elements, then add edges between column elements
    add_edges_from_array_lines(graph, array, transpose=False)
    add_edges_from_array_lines(graph, array, transpose=True)
    return graph


def get_nodes_with_elevations(graph, elevations):
    return (node for node, data in graph.nodes(data=True) if data['elevation'] in elevations)


def run_part_1(graph):
    start_node = next(get_nodes_with_elevations(graph, elevations=['S']))
    end_node = next(get_nodes_with_elevations(graph, elevations=['E']))
    path_length = nx.shortest_path_length(graph, start_node, end_node)
    print(f'Part 1 Path Length: {path_length}')


def run_part_2(graph):
    start_nodes = get_nodes_with_elevations(graph, elevations=['S', 'a'])
    end_node = next(get_nodes_with_elevations(graph, elevations=['E']))
    path_lengths = (nx.shortest_path_length(graph, start_node, end_node) for start_node in start_nodes if
                    nx.has_path(graph, start_node, end_node))
    print(f'Part 2 Path Length: {min(path_lengths)}')


def main():
    graph = get_data()
    run_part_1(graph)
    run_part_2(graph)


if __name__ == '__main__':
    main()
