# https://adventofcode.com/2022/day/3

from dataclasses import dataclass
from functools import reduce

from numpy import intersect1d


@dataclass(frozen=True, order=True)
class Item:
    item_letter: str

    @property
    def priority(self):
        # Predetermined ASCII offsets
        if self.item_letter.isupper():
            return ord(self.item_letter) - 38
        return ord(self.item_letter) - 96


@dataclass
class Rucksack:
    compartment_1: list[Item]
    compartment_2: list[Item]

    @classmethod
    def from_items(cls, items):
        compartment_1 = items[:len(items) // 2]
        compartment_2 = items[len(items) // 2:]
        return cls(compartment_1, compartment_2)

    @property
    def all_items(self):
        return self.compartment_1 + self.compartment_2

    def get_common_item(self):
        # Assumes there is one and only one common item
        return intersect1d(self.compartment_1, self.compartment_2)[0]


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        items_by_rucksack = [[Item(item_letter) for item_letter in items_str.strip()] for items_str in f.readlines()]
        rucksacks = [Rucksack.from_items(items) for items in items_by_rucksack]
    return rucksacks


def run_part_1(rucksacks):
    total_priority = sum([rucksack.get_common_item().priority for rucksack in rucksacks])
    print(f'Part 1 Total Priority: {total_priority}')


def run_part_2(rucksacks, group_size=3):
    # Simplified itertools recipe: https://docs.python.org/3/library/itertools.html#itertools-recipes
    def grouper(iterable, n):
        args = [iter(iterable)] * n
        return zip(*args)

    total_priority = 0
    for rucksack_group in grouper(rucksacks, group_size):
        # Get the items out of our rucksacks
        rucksack_group_items = tuple(rucksack.all_items for rucksack in rucksack_group)
        # Assumes there is one and only one common item
        common_item = reduce(intersect1d, rucksack_group_items)[0]
        total_priority += common_item.priority

    print(f'Part 2 Total Priority: {total_priority}')


def main():
    rucksacks = get_data()
    run_part_1(rucksacks)
    run_part_2(rucksacks)


if __name__ == '__main__':
    main()
