import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    retval = []
    for line in lines:
        retval.append((line[0:int(len(line)/2)], line[int(len(line)/2):]))

    return retval


def part2(input):
    pass


def part1(input):
    priority_map = get_priority_map()
    total = 0
    for c1,c2 in input:
        for l in c1:
            if l in c2:
                # print(f'{l} {priority_map[l]}')
                total += priority_map[l]
                break
    print(total)


def get_priority_map():
    priority_map = dict(map(lambda c: (chr(c), (c-ord('a'))+1), range(ord('a'), ord('z')+1)))
    priority_map.update(dict(map(lambda c: (chr(c), (c - ord('A')) + 27), range(ord('A'), ord('Z')+1))))
    return priority_map

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
