# https://adventofcode.com/2022/day/21

import operator
import sympy
from dataclasses import dataclass

from monkey import Monkey, DumbMonkey, CleverMonkey, Human


@dataclass
class Troop:
    OPERAND_MAP = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    monkeys: dict[str, Monkey]

    @classmethod
    def from_monkey_str_list(cls, monkey_str_list):
        monkeys = {}
        for monkey_str in monkey_str_list:
            monkey_name, monkey_data = monkey_str.split(': ')
            if monkey_data.isnumeric():
                monkey = DumbMonkey(monkey_name, value=int(monkey_data))
            else:
                left_monkey_name, operand_str, right_monkey_name = monkey_data.split(' ')
                operand = cls.OPERAND_MAP[operand_str]
                monkey = CleverMonkey(monkey_name, left_monkey_name, right_monkey_name, operand)
            monkeys[monkey_name] = monkey
        return cls(monkeys)


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        troop = Troop.from_monkey_str_list(f.read().splitlines())
    return troop


def run_part_1(troop, root_monkey_name='root'):
    root_monkey = troop.monkeys[root_monkey_name]
    print(f'Root Monkey Yells: {root_monkey.yell(troop):.0f}')


def run_part_2(troop, root_monkey_name='root', human_name='humn'):
    # Change Monkey 'humn' into a Human
    human = Human(human_name)
    troop.monkeys[human_name] = human

    # Find out what the Left Monkey and Right Monkey from the Root Monkey yell
    root_monkey = troop.monkeys[root_monkey_name]
    left_monkey_yells = troop.monkeys[root_monkey.left_monkey_name].yell(troop)
    right_monkey_yells = troop.monkeys[root_monkey.right_monkey_name].yell(troop)

    # Solve to find out what the Human yelled
    human_yelled = sympy.solve(left_monkey_yells - right_monkey_yells, human_name)[0]
    print(f'Human Yelled: {human_yelled:.0f}')


def main():
    troop = get_data()
    run_part_1(troop)
    run_part_2(troop)


if __name__ == '__main__':
    main()
