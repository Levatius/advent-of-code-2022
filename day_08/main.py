# https://adventofcode.com/2022/day/8

import operator
from dataclasses import dataclass, field
from functools import reduce
from itertools import product, chain


@dataclass
class Tree:
    height: int
    is_visible: bool = False
    scenic_scores: list[int] = field(default_factory=list)

    @property
    def scenic_score(self):
        return reduce(operator.mul, self.scenic_scores, 1)


@dataclass
class Forest:
    trees: list[list[Tree]]

    @classmethod
    def from_height_map(cls, height_map):
        trees = [[Tree(int(height)) for height in height_row] for height_row in height_map.splitlines()]
        forest = cls(trees)
        forest._update_tree_visibilities()
        forest._update_tree_scenic_scores()
        return forest

    def get_tree_lines(self, transpose=False, reverse=False):
        # Default: (transpose=False, reverse=False) refers to viewing the tree lines from the left side
        # Example: (transpose=True, reverse=True) refers to viewing the tree lines from the bottom side
        for tree_line in zip(*self.trees) if transpose else self.trees:
            yield reversed(tree_line) if reverse else tree_line

    def get_tree_lines_from_all_sides(self):
        # Calls get_tree_lines() from all 4 sides by using combinations of "transpose" and "reverse"
        for transpose, reverse in product((False, True), repeat=2):
            yield from self.get_tree_lines(transpose, reverse)

    def _update_tree_visibilities(self):
        # Assumes it is only called once during init
        for tree_line in self.get_tree_lines_from_all_sides():
            max_height = -1
            for tree in tree_line:
                if tree.height <= max_height:
                    continue
                tree.is_visible = True
                max_height = tree.height

    def _update_tree_scenic_scores(self):
        # Assumes it is only called once during init
        # Also must convert to using lists over generators since we need to double dip into tree_line
        for tree_line in map(list, self.get_tree_lines_from_all_sides()):
            for i, tree in enumerate(tree_line):
                scenic_score = 0
                # Look at the other trees behind this tree
                for other_tree in tree_line[i + 1:]:
                    scenic_score += 1
                    if other_tree.height >= tree.height:
                        break
                tree.scenic_scores.append(scenic_score)


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        forest = Forest.from_height_map(f.read())
    return forest


def run(forest):
    total_visible = sum(int(tree.is_visible) for tree in chain.from_iterable(forest.trees))
    print(f'Total Visible: {total_visible}')
    max_scenic_score = max(tree.scenic_score for tree in chain.from_iterable(forest.trees))
    print(f'Max Scenic Score: {max_scenic_score}')


def main():
    forest = get_data()
    run(forest)


if __name__ == '__main__':
    main()
