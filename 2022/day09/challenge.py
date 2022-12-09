import argparse
from copy import copy


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    retval = []
    for line in lines:
        if line:
            direction, distance = line.split()
            retval.append([direction, int(distance)])

    return retval


def part2(data):
    pass


def part1(data):
    rope = RopeHT()
    for line in data:
        rope.do_move(*line)
    print(len(set([tuple(tv) for tv in rope.tail_visited])))


class RopeHT(object):
    def __init__(self):
                             # X,  Y
        self.head_position = [50, 50]  # Just a random starting point
        self.tail_position = [50, 50]
        self.tail_visited = []
        self.tail_visited.append(self.tail_position)

    def do_move(self, direction, move_count):
        move_count += 1  # update now for call to range() in move_by()
        if direction == 'U':
            self.move_by(move_count, 1)
        elif direction == 'D':
            self.move_by(move_count*-1, 1, step_by=-1)
        elif direction == 'L':
            self.move_by(move_count*-1, 0, step_by=-1)
        elif direction == 'R':
            self.move_by(move_count, 0)
        else:
            raise ValueError('wtf?')

    def move_by(self, move, direction_i, step_by=1):
        for i in range(self.head_position[direction_i], self.head_position[direction_i]+move, step_by):
            previous = copy(self.head_position)
            self.head_position[direction_i] = i
            if self.tail_not_touching():
                self.tail_position = previous
                self.tail_visited.append(previous)

    def tail_not_touching(self):
        diffs = [self.head_position[0] - self.tail_position[0], self.head_position[1] - self.tail_position[1]]
        return any([abs(d) > 1 for d in diffs])


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
