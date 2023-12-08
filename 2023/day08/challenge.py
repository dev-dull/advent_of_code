import argparse

from itertools import cycle
from functools import reduce
from collections import defaultdict


# For part 1
class DesertPositioningSystem(object):
    def __init__(self, turns, desert_road, current='AAA'):
        self.turns = cycle(turns)
        self.desert_map = defaultdict(list)
        self.current = current

        for fork in desert_road:
            fork_parts = fork.split(' = ')
            # using += instead of = to preserve pointers that might be useful for part 2
            self.desert_map[fork_parts[0]] += [lr for lr in fork_parts[1][1:-1].split(', ')]

    def __iter__(self):
        # self.current = 'AAA'
        while self.current != 'ZZZ':
            self.current = self.desert_map[self.current][0 if next(self.turns) == 'L' else 1]
            yield self.current

#
class GhostlyPositioningSystem(DesertPositioningSystem):
    def __iter__(self):
        while self.current[-1] != 'Z':
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


def part2(turns, desert_map):
    # I had to seek out what the shortcut was here. I'm dumbstruck that anyone noticed this pattern.
    # Too high: 4397914874557511198709522361
    # Too high: 16722109789192057789770047
    a_listers = list(filter(lambda p: p[-1] == 'A', GhostlyPositioningSystem(turns, desert_map).desert_map.keys()))  # gross line is gross
    steps = [len(turns)]
    for ayy in a_listers:
        gps = GhostlyPositioningSystem(turns, desert_map, current=ayy)
        for i, pos in enumerate(gps):
            continue
        else:
            steps.append(int((i+1)/steps[0]))
    print(reduce(lambda a,b: a*b, steps))


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

    # part1(turns, desert_map)
    part2(turns, desert_map)


if __name__ == '__main__':
    main()
