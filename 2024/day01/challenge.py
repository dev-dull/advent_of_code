import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    rows = [row.split() for row in lines]
    return [int(i[0]) for i in rows],[int(i[1]) for i in rows]


def part2(l, r):
    print(sum([l[i]*r.count(l[i]) for i in range(0,len(l))]))


def part1(l, r):
    l.sort()
    r.sort()
    print(sum([abs(l[i]-r[i]) for i in range(0, len(l))]))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2024 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    #part1(*data)
    part2(*data)


if __name__ == '__main__':
    main()
