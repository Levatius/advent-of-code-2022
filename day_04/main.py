# https://adventofcode.com/2022/day/4

from dataclasses import dataclass


@dataclass
class Assignment:
    start_id: int
    end_id: int

    @classmethod
    def from_assignment_str(cls, assignment_str):
        # Example assignment_str: '3-22'
        return cls(*map(int, assignment_str.split('-')))

    def is_contained_in(self, other):
        is_start_contained = self.start_id >= other.start_id
        is_end_contained = self.end_id <= other.end_id
        return is_start_contained and is_end_contained

    def is_overlapping_with(self, other):
        is_start_overlapping = other.start_id <= self.start_id <= other.end_id
        is_end_overlapping = other.start_id <= self.end_id <= other.end_id
        return is_start_overlapping or is_end_overlapping


@dataclass
class Team:
    assignment_a: Assignment
    assignment_b: Assignment

    @classmethod
    def from_team_str(cls, team_str):
        # Example team_str: '3-22,6-44'
        return cls(*map(Assignment.from_assignment_str, team_str.split(',')))

    def check_fully_contained(self):
        a = self.assignment_a
        b = self.assignment_b
        return a.is_contained_in(b) or b.is_contained_in(a)

    def check_overlap(self):
        a = self.assignment_a
        b = self.assignment_b
        return a.is_overlapping_with(b) or b.is_overlapping_with(a)


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        teams = [Team.from_team_str(team_str) for team_str in f.read().splitlines()]
    return teams


def run(teams):
    total_fully_contained = sum(team.check_fully_contained() for team in teams)
    print(f'Total Fully Contained: {total_fully_contained}')
    total_overlap = sum(team.check_overlap() for team in teams)
    print(f'Total Overlapping: {total_overlap}')


def main():
    teams = get_data()
    run(teams)


if __name__ == '__main__':
    main()
