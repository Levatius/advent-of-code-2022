# https://adventofcode.com/2022/day/11

import math
import numpy as np
import operator
import re
from dataclasses import dataclass
from functools import reduce

SUPPORTED_OPS = {
    '+': operator.add,
    '*': operator.mul
}
INPUT_PATTERN = re.compile(r'''Monkey (?P<monkey_id>\d+):
  Starting items: (?P<starting_items>.*)
  Operation: new = old (?P<operand>[+*]) (?P<operation_value>.*)
  Test: divisible by (?P<test_value>\d+)
    If true: throw to monkey (?P<test_true_monkey_id>\d+)
    If false: throw to monkey (?P<test_false_monkey_id>\d+)''')


@dataclass
class Item:
    worry_level: int

    def do_worry_reduction(self, worry_reduction_mod=None):
        if not worry_reduction_mod:
            self.worry_level //= 3
        else:
            self.worry_level %= worry_reduction_mod


@dataclass
class Operation:
    operand: chr
    value_str: str

    def apply_to(self, other_value):
        value = other_value if self.value_str == 'old' else int(self.value_str)
        return SUPPORTED_OPS[self.operand](value, other_value)


@dataclass
class Test:
    value: int
    true_monkey_id: int
    false_monkey_id: int

    def get_monkey_id(self, value):
        if value % self.value == 0:
            return self.true_monkey_id
        return self.false_monkey_id


@dataclass
class Monkey:
    monkey_id: int
    items: list[Item]
    operation: Operation
    test: Test
    inspections: int = 0

    @classmethod
    def from_monkey_info(cls, monkey_info):
        m = INPUT_PATTERN.match(monkey_info)
        monkey_id = int(m['monkey_id'])
        items = [Item(int(item)) for item in m['starting_items'].split(', ')]
        operation = Operation(m['operand'], m['operation_value'])
        test = Test(int(m['test_value']), int(m['test_true_monkey_id']), int(m['test_false_monkey_id']))
        return cls(monkey_id, items, operation, test)

    def inspect(self, item, worry_reduction_mod):
        self.inspections += 1
        item.worry_level = self.operation.apply_to(item.worry_level)
        item.do_worry_reduction(worry_reduction_mod)
        target_monkey_id = self.test.get_monkey_id(item.worry_level)
        return target_monkey_id


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        monkeys = [Monkey.from_monkey_info(monkey_info) for monkey_info in f.read().split('\n\n')]
    return monkeys


def get_monkey(monkeys, monkey_id):
    return next(monkey for monkey in monkeys if monkey.monkey_id == monkey_id)


def run(monkeys, rounds=20, worry_reduction_mod=None, top=2):
    for _ in range(rounds):
        for monkey in monkeys:
            items_to_throw = []
            # Do inspections
            for item in monkey.items:
                target_monkey_id = monkey.inspect(item, worry_reduction_mod)
                items_to_throw.append((item, target_monkey_id))
            # After inspections, throw items
            for item, target_monkey_id in items_to_throw:
                target_monkey = get_monkey(monkeys, target_monkey_id)
                monkey.items.remove(item)
                target_monkey.items.append(item)

    top_monkeys = sorted(monkeys, key=lambda monkey_: monkey_.inspections, reverse=True)[:top]
    monkey_business = math.prod(monkey.inspections for monkey in top_monkeys)
    print(f'Monkey Business: {monkey_business}')


def main():
    # Part 1
    monkeys = get_data()
    run(monkeys)
    # Part 2
    monkeys = get_data()
    worry_reduction_mod = reduce(np.lcm, (monkey.test.value for monkey in monkeys))
    run(monkeys, rounds=10000, worry_reduction_mod=worry_reduction_mod)


if __name__ == '__main__':
    main()
