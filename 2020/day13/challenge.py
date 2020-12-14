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
    # key == what t%value needs to be
    d = {}
    for k,v in enumerate(input):
        if isinstance(v, int):
            d[k]=v

    # There's clearly an equation that'll solve this problem a lot faster than a loop
    # ...but right now, I'd rather kick things off and watch a documentary while this runs
    ts = 100000000000000  # They told me it'd be bigger than this

    while True:
        found_it = []
        for remainder,bus in d.items():
            found_it.append((ts+remainder)%bus==0)

        if not ts%100000:
            print(ts, end='\r')

        if all(found_it):
            print('\n'+str(ts))
            break
        elif ts > 999999999999999:  # Stop for for the sake of sanity, and my CPU.
            print('fail.')
            break
        ts += 1

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
    #part1(*input)
    part2(input[1])


if __name__ == '__main__':
    main()
