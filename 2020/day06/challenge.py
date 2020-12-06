import argparse
from functools import reduce

class TravelGroup(list):
    def __init__(self, group_data):
        for person_data in group_data.splitlines():
            self.append(person_data)

    def group_yes_count(self):
        return len(set(reduce(lambda a,b: a+b, self)))


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    lines = fin.read().split('\n\n')
    fin.close()

    while '' in lines:
        lines.remove('')

    return lines


def part2(input):
    pass


def part1(input):
    group_data = []
    for gd in input:
        group_data.append(TravelGroup(gd))

    print(sum([gd.group_yes_count() for gd in group_data]))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
