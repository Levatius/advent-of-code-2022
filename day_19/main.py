# https://adventofcode.com/2022/day/19

import re
from copy import deepcopy
from dataclasses import dataclass

BLUEPRINT_PATTERN = re.compile(
    r'Blueprint (?P<id>\d+):'
    r' Each ore robot costs (?P<ore_robot_ore_cost>\d+) ore.'
    r' Each clay robot costs (?P<clay_robot_ore_cost>\d+) ore.'
    r' Each obsidian robot costs (?P<obsidian_robot_ore_cost>\d+) ore and (?P<obsidian_robot_clay_cost>\d+) clay.'
    r' Each geode robot costs (?P<geode_robot_ore_cost>\d+) ore and (?P<geode_robot_obsidian_cost>\d+) obsidian.'
)
RESOURCE_ORE = 'ore'
RESOURCE_CLAY = 'clay'
RESOURCE_OBSIDIAN = 'obsidian'
RESOURCE_GEODE = 'geode'


@dataclass
class RobotFactory:
    id: int
    robot_costs: dict

    @classmethod
    def from_blueprint(cls, blueprint):
        m = BLUEPRINT_PATTERN.match(blueprint)
        robot_factory_id = int(m['id'])
        robot_costs = {
            RESOURCE_ORE: {RESOURCE_ORE: int(m['ore_robot_ore_cost'])},
            RESOURCE_CLAY: {RESOURCE_ORE: int(m['clay_robot_ore_cost'])},
            RESOURCE_OBSIDIAN: {
                RESOURCE_ORE: int(m['obsidian_robot_ore_cost']),
                RESOURCE_CLAY: int(m['obsidian_robot_clay_cost'])
            },
            RESOURCE_GEODE: {
                RESOURCE_ORE: int(m['geode_robot_ore_cost']),
                RESOURCE_OBSIDIAN: int(m['geode_robot_obsidian_cost'])
            }
        }
        return cls(robot_factory_id, robot_costs)

    def is_robot_buildable(self, robot_type, state):
        for resource, cost in self.robot_costs[robot_type].items():
            if state.inventory[resource] < cost:
                return False
        return True

    def sufficient_amount_of(self, resource_type, state):
        resource_end_total = state.inventory[resource_type] + state.robots[resource_type] * state.remaining_minutes
        # The default of 1000 creates a constant demand for geodes
        resource_max_cost = max((cost[resource_type] for cost in self.robot_costs.values() if cost.get(resource_type)),
                                default=1000)
        resource_max_usage = resource_max_cost * state.remaining_minutes
        return resource_end_total >= resource_max_usage

    def get_build_list(self, state):
        return [resource_type for resource_type in [RESOURCE_ORE, RESOURCE_CLAY, RESOURCE_OBSIDIAN, RESOURCE_GEODE] if
                not self.sufficient_amount_of(resource_type, state)]

    def build_robot(self, robot_type, state):
        robot_cost = self.robot_costs[robot_type]
        for resource, cost in robot_cost.items():
            state.inventory[resource] -= cost
        state.robots[robot_type] += 1


@dataclass
class State:
    inventory: dict
    robots: dict
    remaining_minutes: int
    geode_total: int = 0

    def harvest_resources(self):
        for robot_type, quantity in self.robots.items():
            self.inventory[robot_type] += quantity

    def pass_time(self):
        self.remaining_minutes -= 1
        if self.remaining_minutes == 0:
            self.geode_total = self.inventory[RESOURCE_GEODE]


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        robot_factories = [RobotFactory.from_blueprint(blueprint) for blueprint in f.read().splitlines()]
    return robot_factories


def simulate(robot_factory: RobotFactory, old_state: State):
    geode_totals = []
    for robot_type_to_build in robot_factory.get_build_list(old_state):
        state = deepcopy(old_state)

        # Fast forward until we can build our desired robot
        while not robot_factory.is_robot_buildable(robot_type_to_build, state) and state.remaining_minutes > 0:
            state.harvest_resources()
            state.pass_time()

        # If time remains, harvest resources and build our new robot
        if state.remaining_minutes > 0:
            state.harvest_resources()
            robot_factory.build_robot(robot_type_to_build, state)
            state.pass_time()

        # If time remains, build the remainder of our robots recursively
        if state.remaining_minutes > 0:
            state.geode_total = simulate(robot_factory, state)

        geode_totals.append(state.geode_total)
    return max(geode_totals)


def run(robot_factories, total_minutes, top=None):
    total_quality = 0
    for robot_factory in robot_factories[:top]:
        starting_state = State(
            inventory={RESOURCE_ORE: 0, RESOURCE_CLAY: 0, RESOURCE_OBSIDIAN: 0, RESOURCE_GEODE: 0},
            robots={RESOURCE_ORE: 1, RESOURCE_CLAY: 0, RESOURCE_OBSIDIAN: 0, RESOURCE_GEODE: 0},
            remaining_minutes=total_minutes
        )
        geode_max = simulate(robot_factory, starting_state)
        print(f'Blueprint ID: {robot_factory.id}, Geode Max: {geode_max}')
        total_quality += robot_factory.id * geode_max
    print(f'Total Quality: {total_quality}')


def main():
    robot_factories = get_data()
    run(robot_factories, total_minutes=24)
    run(robot_factories, total_minutes=32, top=3)


if __name__ == '__main__':
    main()
