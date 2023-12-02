import argparse
from collections import defaultdict

def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    return lines

NUMBER_NAMES = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def find_first_numeric(calibration_string):
    for c in calibration_string:
        if c.isnumeric():
            return c

def part2(data):
    fixed_data = []
    for line in data:
        insertions = defaultdict(list)
        for i, c in enumerate(line):
            for number_name in NUMBER_NAMES.keys():
                try:
                    insertions[number_name].append(line[i:].index(number_name) + i)
                except ValueError:
                    continue

        fixed_line = list(line)
        for number_name, number_insertions in insertions.items():
            for number_insertion in number_insertions:
                fixed_line[number_insertion] = NUMBER_NAMES[number_name]
        fixed_data.append(''.join(fixed_line))

    part1(fixed_data)

def part1(data):
    values = []
    for line in data:
        first = find_first_numeric(line)
        last = find_first_numeric(line[::-1])
        values.append(int(f'{first}{last}'))
    print(sum(values))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
