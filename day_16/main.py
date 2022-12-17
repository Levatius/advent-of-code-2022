# https://adventofcode.com/2022/day/16

import networkx as nx
import re
from dataclasses import dataclass
from more_itertools import set_partitions
from time import time


@dataclass
class Valve:
    name: str
    flow_rate: int
    linked_valve_names: list[str]

    @classmethod
    def from_readout_str(cls, readout_str):
        readout_pattern = re.compile(
            r'Valve (?P<name>\w+) has flow rate=(?P<flow_rate>\d+); '
            r'tunnel[s]* lead[s]* to valve[s]* (?P<linked_valve_names>.+)'
        )
        m = readout_pattern.match(readout_str)
        return cls(m['name'], int(m['flow_rate']), m['linked_valve_names'].split(', '))

    def __hash__(self):
        return hash(self.name)


class TunnelNetwork(nx.Graph):
    cached_path_lengths: dict

    @classmethod
    def from_valves(cls, valves):
        tunnel_network = cls()
        for valve in valves:
            for linked_valve_name in valve.linked_valve_names:
                linked_valve = next(valve for valve in valves if valve.name == linked_valve_name)
                tunnel_network.add_edge(valve, linked_valve)
        # Cache all shortest path lengths
        tunnel_network.cached_path_lengths = dict(nx.all_pairs_shortest_path_length(tunnel_network))
        return tunnel_network

    def get_valve(self, name):
        return next(valve for valve in self.nodes if valve.name == name)

    def traverse(self, current_valve, remaining_valves, remaining_minutes):
        # Remove the current valve from the remaining valves
        remaining_valves = [valve for valve in remaining_valves if valve.name != current_valve.name]
        pressures = []
        for valve in remaining_valves:
            # Deduct the cost of moving to the valve and opening it
            new_remaining_minutes = remaining_minutes - self.cached_path_lengths[current_valve][valve] - 1

            # If we still have time, contribute pressure and then continue on from this valve
            if new_remaining_minutes > 0:
                pressure = new_remaining_minutes * valve.flow_rate
                pressure += self.traverse(valve, remaining_valves, new_remaining_minutes)
                pressures.append(pressure)
        return max(pressures, default=0)

    def calc_max_pressure(self, starting_valve, remaining_valves, remaining_minutes, worker_count):
        max_pressure = 0
        for remaining_valves_subsets in set_partitions(remaining_valves, worker_count):
            # Imbalanced subsets are unlikely to yield an optimal solution, skip them
            if max(map(len, remaining_valves_subsets)) - min(map(len, remaining_valves_subsets)) > 1:
                continue

            # Calculate total pressure across all workers
            total_pressure = 0
            for remaining_valves_subset in remaining_valves_subsets:
                total_pressure += self.traverse(starting_valve, remaining_valves_subset, remaining_minutes)
            max_pressure = max(max_pressure, total_pressure)
        return max_pressure


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        valves = list(map(Valve.from_readout_str, f.read().splitlines()))
    return TunnelNetwork.from_valves(valves)


def run(tunnel_network, remaining_minutes, worker_count=1):
    start_time = time()
    starting_valve = tunnel_network.get_valve('AA')
    remaining_valves = (valve for valve in tunnel_network.nodes if valve.flow_rate > 0)
    max_pressure = tunnel_network.calc_max_pressure(starting_valve, remaining_valves, remaining_minutes, worker_count)
    print(f'Max pressure in {remaining_minutes} minutes with {worker_count} worker(s): {max_pressure}')
    print(f'Calculated in {time() - start_time:.2f} seconds')


def main():
    tunnel_network = get_data()
    run(tunnel_network, remaining_minutes=30)
    run(tunnel_network, remaining_minutes=26, worker_count=2)
    # For fun, assuming we can train both elephants at the same time
    run(tunnel_network, remaining_minutes=26, worker_count=3)


if __name__ == '__main__':
    main()
