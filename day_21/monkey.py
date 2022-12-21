import operator
from dataclasses import dataclass

from sympy import Symbol


@dataclass
class Monkey:
    name: str

    def yell(self, troop):
        pass


@dataclass
class DumbMonkey(Monkey):
    value: int

    def yell(self, troop):
        return self.value


@dataclass
class CleverMonkey(Monkey):
    left_monkey_name: str
    right_monkey_name: str
    operand: operator

    def yell(self, troop):
        left_monkey = troop.monkeys[self.left_monkey_name]
        right_monkey = troop.monkeys[self.right_monkey_name]
        return self.operand(left_monkey.yell(troop), right_monkey.yell(troop))


@dataclass
class Human(Monkey):
    def yell(self, troop):
        return Symbol(self.name)
