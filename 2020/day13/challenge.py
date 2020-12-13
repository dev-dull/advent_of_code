import argparse

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

    return int(lines[0]),[n if n=='x' else int(n) for n in lines[1].split(',')]


def part2(input):
    pass


def part1(ts, sched):
    sched = list(filter(lambda n: isinstance(n, int), sched))
    time_index = 0
    while True:
        time_index += 1
        busses_now = list(filter(lambda b: time_index%b==0, sched))
        if busses_now and time_index >= ts:
            print('%s * %s = %s' % (min(busses_now), time_index-ts, (time_index-ts) * min(busses_now)))
            break


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(*input)
    #part2(input)


if __name__ == '__main__':
    main()
