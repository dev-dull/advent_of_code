import argparse
from itertools import cycle
from collections import defaultdict


class DesertPositioningSystem(object):
    def __init__(self, turns, desert_road):
        self.turns = cycle(turns)
        self.desert_map = defaultdict(list)

        for fork in desert_road:
            fork_parts = fork.split(' = ')
            # using += instead of = to preserve pointers that might be useful for part 2
            self.desert_map[fork_parts[0]] += [lr for lr in fork_parts[1][1:-1].split(', ')]

    def __iter__(self):
        self.current = 'AAA'
        while self.current != 'ZZZ':
            self.current = self.desert_map[self.current][0 if next(self.turns) == 'L' else 1]
            yield self.current


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        parts = fin.read().strip().split('\n\n')

    return parts[0], parts[1].splitlines()


def part2(data):
    pass


def part1(turns, desert_map):
    dps = DesertPositioningSystem(turns, desert_map)
    for i, pos in enumerate(dps):
        continue
    else:
        print(i+1)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    turns, desert_map = get_input(args.test)

    part1(turns, desert_map)
    #part2(data)


if __name__ == '__main__':
    main()
