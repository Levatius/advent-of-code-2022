# https://adventofcode.com/2022/day/13

import ast
import math
from dataclasses import dataclass
from more_itertools import windowed
from itertools import zip_longest


@dataclass
class Packet:
    items: list
    is_divider: bool = False

    def compare(self, left, right):
        # Example: 2 vs 4
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True
            elif left > right:
                return False
        # Example: None vs 4 (left is out of elements)
        elif left is None:
            return True
        # Example: 2 vs None (right is out of elements)
        elif right is None:
            return False
        # Example: 2 vs [4, 5, 6]
        elif isinstance(left, int) and isinstance(right, list):
            return self.compare([left], right)
        # Example: [2, 3] vs 4
        elif isinstance(left, list) and isinstance(right, int):
            return self.compare(left, [right])
        # Example: [2, 3] vs [4, 5, 6]
        elif isinstance(left, list) and isinstance(right, list):
            for left, right in zip_longest(left, right):
                result = self.compare(left, right)
                # Continue until we reach a definitive result
                if result is None:
                    continue
                return result

    def __lt__(self, other):
        return self.compare(self.items, other.items)


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        packets = [Packet(ast.literal_eval(input_str)) for input_str in f.read().splitlines() if input_str != '']
    return packets


def run_part_1(packets):
    pairwise_comparisons = (i for i, packet_pair in enumerate(windowed(packets, n=2, step=2), start=1) if
                            packet_pair[0] < packet_pair[1])
    print(f'Pairwise Total: {sum(pairwise_comparisons)}')


def run_part_2(packets):
    divider_indices = (i for i, packet in enumerate(sorted(packets), start=1) if packet.is_divider)
    print(f'Decoder Key: {math.prod(divider_indices)}')


def main():
    packets = get_data()
    run_part_1(packets)
    # Add divider packets for part 2
    packets += [Packet([[2]], is_divider=True), Packet([[6]], is_divider=True)]
    run_part_2(packets)


if __name__ == '__main__':
    main()
