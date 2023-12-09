import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    int_lines = []
    for line in lines:
        int_lines.append([int(i) for i in line.split()])

    return int_lines


def part2(data):
    patterns_sum = 0
    for pattern in data:
        pattern.reverse()
        patterns_sum += pattern[-1] + pattern_parser(pattern)
    print(patterns_sum)


def pattern_parser(pattern):
    next_pattern = [pattern[i+1]-p for i,p in enumerate(pattern[:-1])]
    if any(next_pattern):
        return next_pattern[-1] + pattern_parser(next_pattern)
    return 0


def part1(data):
    patterns_sum = 0
    for pattern in data:
        patterns_sum += pattern[-1] + pattern_parser(pattern)
    print(patterns_sum)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
