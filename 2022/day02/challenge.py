import argparse
from functools import partial


ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissors'


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    lines = fin.read().splitlines()
    fin.close()

    return lines


def part2(input):
    strat = rps_strategy_p2()
    total = 0
    for line in input:
        rival_choice, my_choice = line.split()
        total += getattr(strat, my_choice)(rival_choice)
    print(total)


def part1(input):
    strat = rps_strategy_p1()
    total = 0
    for line in input:
        rival_choice, my_choice = line.split()
        total += getattr(strat, my_choice)(rival_choice)
    print(total)


class rps_strategy_p1(object):
    def __init__(self):
        # Confusing mappings so I can (hopefully) just swap out whatever I need to for part 2
        self.X = partial(self.score_round, 1)  # Rock
        self.Y = partial(self.score_round, 2)  # Paper
        self.Z = partial(self.score_round, 3)  # Scissors

        self._OPTIONS_MAP = {
            1: ROCK,
            2: PAPER,
            3: SCISSORS,
            'A': ROCK,
            'B': PAPER,
            'C': SCISSORS
        }

        self._WIN_LOSE_MAP = {
            ROCK: (SCISSORS, PAPER),
            PAPER: (ROCK, SCISSORS),
            SCISSORS: (PAPER, ROCK)
        }

    def score_round(self, base_score, rival_choice):
        # test win condition:
        if self._WIN_LOSE_MAP[self._OPTIONS_MAP[base_score]][0] == self._OPTIONS_MAP[rival_choice]:
            return 6 + base_score
        elif self._WIN_LOSE_MAP[self._OPTIONS_MAP[base_score]][1] == self._OPTIONS_MAP[rival_choice]:
            return base_score

        return 3 + base_score


class rps_strategy_p2(rps_strategy_p1):
    # My efforts in part 1 to make part 2 easier backfired a little, and now this solution is WILDLY over-engineered.
    def __init__(self):
        super().__init__()

        # Reverse the _OPTIONS_MAP from the p1 object so I can find the value to pass to score_round()
        self._SCORE_MAP = {}
        for k, v in self._OPTIONS_MAP.items():
            if isinstance(k, int):
                self._SCORE_MAP[v] = k

        self.X = partial(self.pick_move, 0)  # lose
        self.Y = self.draw  # draw
        self.Z = partial(self.pick_move, 1)  # win

    def pick_move(self, i, rival_choice):
        move = self._SCORE_MAP[self._WIN_LOSE_MAP[self._OPTIONS_MAP[rival_choice]][i]]
        return self.score_round(move, rival_choice)

    def draw(self, rival_choice):
        move = self._SCORE_MAP[self._OPTIONS_MAP[rival_choice]]
        return self.score_round(move, rival_choice)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    # part1(input)
    part2(input)


if __name__ == '__main__':
    main()
