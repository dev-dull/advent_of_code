import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    return lines


def part2(input):
    pass


def part1(input):
    for data_string in input:
        frame = [0, 4]
        leni = len(data_string)  # Hello, this is Lenny.

        while frame[1]+1 < leni:
            if len(set(data_string[frame[0]:frame[1]])) == len(data_string[frame[0]:frame[1]]):
                print(data_string[frame[0]:frame[1]], data_string[frame[1]-1],frame[1])
                break
            frame = [n+1 for n in frame]


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
