import argparse

class xmas(list):
    def __init__(self, data, preamble_len):
        super().__init__(data[preamble_len:])
        self._window_start = 0
        self._window_end = preamble_len

    def __next__(self):
        v = self[self._window_end]
        window = self[self._window_start:self._window_end]
        self._window_start += 1
        self._window_end += 1
        for i in range(0,len(window)-1):
            if v-window[i] in window[i+1:]:
                return v,True
        return v,False

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

    retval = [int(n) for n in lines]
    return retval


def part2(input):
    pass


def part1(input):
    valid = True
    while valid:
        n,valid = next(input)
    print('invalid:', n)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = xmas(get_input(args.test), 5 if args.test else 25)
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
