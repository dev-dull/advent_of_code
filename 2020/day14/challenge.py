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

    return lines


class MemDock(dict):
    def __init__(self):
        self.mask = []

    def set_mask(self, mask):
        self.mask = list(mask)
        self.mask.reverse()  # put least significant digit at index 0

    def __setitem__(self, key, val):
        for i,op in enumerate(self.mask):
            if op == '1' and not val & pow(2, i):
                val += pow(2, i)
            if op == '0' and val & pow(2, i):
                val -= pow(2, i)
        self.update({key:val})


def part2(input):
    pass


def part1(input):
    md = MemDock()
    for line in input:
        if line.startswith('mask'):
            md.set_mask(line.split()[-1])
        else:
            sl = line.split()
            key = int(sl[0].split('[')[-1][0:-1])
            val = int(sl[-1])
            md[key] = val

    print(sum(md.values()))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
