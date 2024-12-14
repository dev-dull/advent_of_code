import os
import argparse
from time import sleep
from itertools import cycle


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = [[l for l in line] for line in fin.read().strip().splitlines()]

    return lines


class LabMap(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
                                    #  up     right   down     left
        self._next_direction = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])

        self.map_size = (len(self), len(self[0]))
        self.move_direction = next(self._next_direction)
        self.guard_position = self._find_guard()
        self[self.guard_position[0]][self.guard_position[1]] = 'X'

    def _find_guard(self):
        for ri, row in enumerate(self):
            try:
                return (ri, row.index('^'))
            except ValueError:
                continue

    def _check_position(self, r, c):
        return -1 < r < self.map_size[0] and -1 < c < self.map_size[1]

    def __call__(self):
        next_r = self.guard_position[0]+self.move_direction[0]
        next_c = self.guard_position[1]+self.move_direction[1]
        if not self._check_position(next_r, next_c):
            return False

        # looking at the input, I think the guard could spin in a 360 before moving again
        while self[next_r][next_c] == '#':
            self.move_direction = next(self._next_direction)
            next_r = self.guard_position[0]+self.move_direction[0]
            next_c = self.guard_position[1]+self.move_direction[1]

        if self._check_position(next_r, next_c):
            self.guard_position = (next_r, next_c)
            self[next_r][next_c] = 'X'
            return True
        return False

    def __str__(self):
        lines = []
        for l in self:
            lines.append(''.join(l))
        return '\n'.join(lines)



def part2(data):
    pass


def part1(data):
    animated = False
    map = LabMap(data)
    while map():
        if animated:
            os.system('clear')
            print(map)
            sleep(0.01)
    print(str(map).count('X'))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2024 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    parser.add_argument('-2', '--part2', dest='part2', action='store_true', default=False, help='Run part 2 instead of part 1')
    args = parser.parse_args()
    data = get_input(args.test)

    f = part2 if args.part2 else part1
    f(data)


if __name__ == '__main__':
    main()
