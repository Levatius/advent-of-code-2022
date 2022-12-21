# https://adventofcode.com/2022/day/20

from dataclasses import dataclass


@dataclass
class Item:
    id: int
    value: int


def get_data(file_name='input.txt', decryption_key=1):
    with open(file_name) as f:
        return [Item(i, int(number_str) * decryption_key) for i, number_str in enumerate(f.read().splitlines())]


def run(items, mix_count=1):
    mixed_items = items.copy()
    for _ in range(mix_count):
        for item in items:
            current_index = mixed_items.index(item)
            mixed_item = mixed_items.pop(current_index)
            new_index = (current_index + mixed_item.value) % len(mixed_items)
            mixed_items.insert(new_index, mixed_item)

    zero_index = next(i for i, item in enumerate(mixed_items) if item.value == 0)
    grove_total = sum(mixed_items[(zero_index + (i + 1) * 1000) % len(mixed_items)].value for i in range(3))
    print(f'Grove Total: {grove_total}')


def main():
    items = get_data()
    run(items)
    items = get_data(decryption_key=811589153)
    run(items, mix_count=10)


if __name__ == '__main__':
    main()
