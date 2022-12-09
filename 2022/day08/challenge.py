import argparse
from copy import copy
from functools import reduce


class InvisibleTree(int):
    visible = False
    # Intially, I had score as a list, which made it pass-by-ref, which
    # means that ALL InvisibleTree() pointed at the SAME list
    score = 1


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
    check_east(data)
    data = rot90(data)
    check_east(data)
    data = rot90(data)
    check_east(data)
    data = rot90(data)
    check_east(data)

    best_score = 0
    for row in data:
        for tree in row:
            if tree.score > best_score:
                best_score = tree.score

    print(best_score)


def check_east(data):
    row_len = len(data)
    col_len = len(data[0])

    for ri in range(1, row_len-1):
        for ci in range(1, col_len-1):
            tree_score = 0
            for tree in data[ri][ci+1:]:
                if tree < data[ri][ci]:
                    tree_score += 1
                else:
                    tree_score += 1
                    break
            data[ri][ci].score *= tree_score


def part1(data):
    # I was trying to avoid loops that come into the 2d array from different directions, but
    # that would've been easier and faster to write.
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
    # numpy.rot90() changes my type from InvisibleTree to numpy.int64 and I don't know how to tell numpy to knock it off
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
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
