# https://adventofcode.com/2022/day/2

from dataclasses import dataclass


@dataclass
class Shape:
    SHAPE_LETTER_TO_SCORE_MAP = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}

    shape_letter: str

    @property
    def score(self):
        return self.SHAPE_LETTER_TO_SCORE_MAP[self.shape_letter]


# Part 1 Round Class
@dataclass
class Round:
    opponent_shape: Shape
    your_shape: Shape

    @property
    def score(self):
        # Check for win
        if (self.your_shape.score - 1) % 3 == self.opponent_shape.score % 3:
            return 6 + self.your_shape.score
        # Check for loss
        elif (self.your_shape.score + 1) % 3 == self.opponent_shape.score % 3:
            return 0 + self.your_shape.score
        # Check for draw
        elif self.your_shape.score == self.opponent_shape.score:
            return 3 + self.your_shape.score


# Part 2 Round Class
@dataclass
class CookedRound:
    opponent_shape: Shape
    desired_outcome: str

    @property
    def score(self):
        match self.desired_outcome:
            # Create a win
            case 'Z':
                return 6 + self.opponent_shape.score % 3 + 1
            # Create a loss
            case 'X':
                return 0 + (self.opponent_shape.score + 1) % 3 + 1
            # Create a draw
            case 'Y':
                return 3 + self.opponent_shape.score


def get_data(file_name='input.txt', part=1):
    with open(file_name) as f:
        letters_by_round = (round_str.strip().split(' ') for round_str in f.readlines())
        match part:
            case 1:
                rounds = [Round(Shape(letters[0]), Shape(letters[1])) for letters in letters_by_round]
            case 2:
                rounds = [CookedRound(Shape(letters[0]), letters[1]) for letters in letters_by_round]
    return rounds


def run(rounds):
    total_score = sum([round_.score for round_ in rounds])
    print(f'Total Score: {total_score}')


def main():
    rounds = get_data()
    run(rounds)
    cooked_rounds = get_data(part=2)
    run(cooked_rounds)


if __name__ == '__main__':
    main()
