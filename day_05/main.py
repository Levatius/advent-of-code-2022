# https://adventofcode.com/2022/day/5

import re
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Stack:
    stack_id: int
    crates: list[chr]

    @classmethod
    def from_column(cls, column):
        stack_id = int(column[0])
        crates = [crate for crate in column[1:] if crate != ' ']
        return cls(stack_id, crates)


@dataclass
class Procedure:
    quantity: int
    source_id: int
    target_id: int

    @classmethod
    def from_procedure_str(cls, procedure_str):
        m = re.match(r'move (?P<quantity>\d+) from (?P<source_id>\d+) to (?P<target_id>\d+)', procedure_str)
        return cls(*map(int, m.groups()))


@dataclass
class Ship:
    stacks: list[Stack]

    @classmethod
    def from_deck_layout_str(cls, deck_layout_str):
        deck_layout = deck_layout_str.splitlines()
        # Reverse and transpose the deck layout
        deck_layout.reverse()
        deck_layout = list(map(list, zip(*deck_layout)))
        stacks = [Stack.from_column(column) for column in deck_layout if column[0].isdigit()]
        return cls(stacks)

    @property
    def top_crate_code(self):
        top_crates = [stack.crates[-1] for stack in self.stacks]
        return ''.join(top_crates)

    def get_stack(self, stack_id):
        # Avoiding reliance on the implementation detail that the stacks happen to be in order
        return next(stack for stack in self.stacks if stack.stack_id == stack_id)

    def operate_crane(self, procedure, crane_model):
        source_stack = self.get_stack(procedure.source_id)
        target_stack = self.get_stack(procedure.target_id)

        match crane_model:
            case 9000:
                for _ in range(procedure.quantity):
                    crate = source_stack.crates.pop()
                    target_stack.crates.append(crate)
            case 9001:
                crates = source_stack.crates[-procedure.quantity:]
                source_stack.crates = source_stack.crates[:-procedure.quantity]
                target_stack.crates += crates


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        deck_layout_str, procedures_str = f.read().split('\n\n')
        ship = Ship.from_deck_layout_str(deck_layout_str)
        procedures = [Procedure.from_procedure_str(procedure_str) for procedure_str in procedures_str.splitlines()]
    return ship, procedures


def run(ship, procedures, crane_model=9000):
    for procedure in procedures:
        ship.operate_crane(procedure, crane_model)
    print(f'Message: {ship.top_crate_code}')


def main():
    ship, procedures = get_data()
    run(deepcopy(ship), procedures)
    run(deepcopy(ship), procedures, crane_model=9001)


if __name__ == '__main__':
    main()
