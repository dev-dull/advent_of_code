import argparse
from copy import copy
from collections import defaultdict


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    lines = fin.read().splitlines()
    fin.close()

    while '' in lines:
        lines.remove('')

    return [int(n) for n in lines]

def _part2(input):
    ### NOT working yet. I know I'm on the right track, though.
    ## I need to pin down the cause of doups
    ## I need to include the very first combo (the one with everything)
    for i in range(1, len(input)-1):
        #if input[i-1] - input[i] == 1 and input[i] - input[i+1] == 1:
        if input[i+1] - input[i-1] <= 3:
            c = copy(input)
            c.remove(input[i])
            _part2(c)
            print(input)


def part2(input):
    input.append(max(input)+3)
    input.append(0)
    input.sort()

    _part2(input)


def part1(input):
    diffs = defaultdict(lambda: 0)
    input.append(max(input)+3)
    input.append(0)
    input.sort(reverse=True)  # Lazy, but given valid input, should always work.
    for i in range(0, len(input)-1):  # I'm mildly annoyed that these problems always force me into C-style loops.
        diffs[input[i] - input[i+1]] += 1

    for k,v in diffs.items():
        print(k, v)  # if our defaultdict contains a key other than 1, 2, or 3, then we know sort() didn't cut it.

    print('%s * %s = %s' % (diffs[1], diffs[3], diffs[1]*diffs[3]))



def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    #part1(input)
    part2(input)


if __name__ == '__main__':
    main()
