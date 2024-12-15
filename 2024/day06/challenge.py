import os
import argparse
from time import sleep
from copy import deepcopy
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

    def check_for_turn(self, r, c):
        return self[r][c] == '#'

    def __call__(self):
        next_r = self.guard_position[0]+self.move_direction[0]
        next_c = self.guard_position[1]+self.move_direction[1]
        if (next_r, next_c) == (7, 32) and self[7][33]=='O':
            print('', end='')
        if not self._check_position(next_r, next_c):
            return False

        # looking at the input, I think the guard could spin in a 360 before moving again
        while self.check_for_turn(next_r, next_c):
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


class LabMapLoop(LabMap):
    class PatrolLoopException(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._turn_counter = {}

    def check_for_turn(self, r, c):
        if self[r][c] in '#O':
            if (r, c) not in self._turn_counter:
                self._turn_counter[(r, c)] = [0, None]
            elif self._turn_counter[(r, c)][0] == 2 and self._turn_counter[(r, c)][1] == self.move_direction:
                raise self.PatrolLoopException('Loop detected')
            self._turn_counter[(r, c)][0] += 1
            self._turn_counter[(r, c)][1] = self.move_direction
        return self[r][c] in '#O'

    def add_obstruction(self, r, c):
        if self[r][c] == '#' or self.guard_position == (r, c):
            return False
        self[r][c] = 'O'
        return True


def part2(data):
    # Putting an O at 7,33 redirected the guard into a loop created of '#' which
    # broke my old loop detection that only tracked loops against added blocker 'O'
    try:
        animated = False
        loop_positions = []
        for ri in range(len(data)):
            for ci in range(len(data[0])):
                map = LabMapLoop(deepcopy(data))  # I was surprised that 'deepcopy()' was required here
                if map.add_obstruction(ri, ci):
                    try:
                        if (ri, ci) == (7, 33):
                            print('', end='')
                        while map():
                            if animated:
                                os.system('clear')
                                print(map)
                                sleep(0.01)
                    except LabMapLoop.PatrolLoopException:
                        loop_positions.append((ri, ci))
                if not animated:
                    print(f'{map.guard_position[0]:>3d},{map.guard_position[1]:>3d} {ri:>3d}, {ci:>3d} = {int(((ri+1)/len(data))*100):>3d}%', end='\033[0K\r')
    except KeyboardInterrupt as e:
        print(f'{map.guard_position[0]:>3d},{map.guard_position[1]:>3d} {ri:>3d}, {ci:>3d} = {int(((ri+1)/len(data))*100):>3d}%', end='\n\033[0K\r')
        print(map, '\n\n')
        raise e
    print('')
    print(len(loop_positions))


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
