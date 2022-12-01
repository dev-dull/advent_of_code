import argparse
from collections import defaultdict

def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    lines = fin.read().splitlines()
    fin.close()

    retval = defaultdict(list)
    elfi = 0
    for line in lines:
        if line:
            retval[elfi].append(int(line))
        else:
            elfi += 1

    return retval


def part2(input):
    elfi_calories = [(e,sum(c)) for e,c in input.items()]
    elfi_calories.sort(key=lambda elfcal: elfcal[1])
    print(sum([ec[1] for ec in elfi_calories[-3:]]))


def part1(input):
    elfi_calories = dict([(e,sum(c)) for e,c in input.items()])
    max_cal = 0
    max_cal_elf = 0
    for k,v in elfi_calories.items():
        if v > max_cal:
            max_cal = v
            max_cal_elf = k
    print(max_cal_elf, max_cal)

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    # part1(input)
    part2(input)


if __name__ == '__main__':
    main()
