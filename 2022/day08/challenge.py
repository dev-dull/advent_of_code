import argparse
from copy import copy


class InvisibleTree(int):
    visible = False


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    # I'm preemptively assuming that I've got a newline at EOF that'll shoot me in the foot later.
    while '' in lines:
        lines.remove('')

    retval = []
    for line in lines:
        retval.append([InvisibleTree(c) for c in line])
    return retval


def part2(data):
    pass


def part1(data):
    find_left(data)
    data = rot90(data)
    find_left(data)
    data = rot90(data)
    find_left(data)
    data = rot90(data)
    find_left(data)

    ct = 0
    for row in data:
        for tree in row:
            if tree.visible:
                ct += 1
    print(ct)


def find_left(data):
    for line in data:
        previous = -1
        for tree in line:
            if tree > previous:
                tree.visible = True
                previous = tree


def rot90(data, turn_ct=1):
    # Copypasta from AoC 2020 day 20. Don't ask me how this works.
    row_ct = len([t[0] for t in data])
    for _ in range(0, turn_ct):
        rotated_tile = []
        for rn in range(0, row_ct):
            new_row = [t[rn] for t in data[-1::-1]]
            rotated_tile.append(new_row)
        data = copy(rotated_tile)
    return data


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
