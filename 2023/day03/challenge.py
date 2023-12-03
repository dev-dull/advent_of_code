import re
import argparse
from collections import defaultdict
from functools import reduce


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


def get_border_points(start, end, row, width, height):
    border = []
    exclude = []
    for x in range(start, end):
        exclude.append((x, row))

    for x in range(start-1, end+1):
        for y in range(row-1, row+2):
            if (x,y) not in exclude and x >= 0 and x < width and y >= 0 and y < height:
                border.append((x,y))
    return border


def part2(schematic):
    # mostly copy-pasta of part1(). See lines marked with ###
    width = len(schematic[0])
    height = len(schematic)

    gearsets = defaultdict(list)  ### changed type
    for ri, row in enumerate(schematic):
        for match in re.finditer('[0-9]+', row):
            match_start, match_end = match.span()
            for x,y in get_border_points(match_start, match_end, ri, width, height):
                if schematic[y][x] == '*':  ### changed what is matched on
                    gearsets[(x,y)].append(int(match.group(0)))  ### save value based on '*' location
                    break

    ### Calculate the gear ratios to be summed
    gear_ratios = []
    for gearset in filter(lambda g: len(g)>1, gearsets.values()):
        gear_ratios.append(reduce(lambda a,b: a*b, gearset, 1))
    print(sum(gear_ratios))


def part1(schematic):
    width = len(schematic[0])
    height = len(schematic)
    symbols = set(re.sub('\.|[0-9]', '', ''.join(schematic)))

    part_numbers = []
    for ri, row in enumerate(schematic):
        for match in re.finditer('[0-9]+', row):
            match_start, match_end = match.span()
            for x,y in get_border_points(match_start, match_end, ri, width, height):
                if schematic[y][x] in symbols:
                    part_numbers.append(int(match.group(0)))
                    break

    print(sum(part_numbers))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
