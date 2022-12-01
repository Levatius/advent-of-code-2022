# https://adventofcode.com/2022/day/1

from dataclasses import dataclass


@dataclass
class Elf:
    items: list

    @property
    def total_calories(self):
        return sum(self.items)


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        items_by_elf = (items_by_elf_str.split('\n') for items_by_elf_str in f.read().split('\n\n'))
        items_by_elf = ([int(item) for item in items] for items in items_by_elf)
        elves = [Elf(items) for items in items_by_elf]
    return elves


def run(elves, top=1):
    sorted_elves = sorted(elves, key=lambda elf: elf.total_calories, reverse=True)
    top_elves = sorted_elves[:top]
    top_total_calories = sum((top_elf.total_calories for top_elf in top_elves))
    print(f'{top_total_calories} Calories')


if __name__ == '__main__':
    elves = get_data()
    run(elves)
    run(elves, top=3)
