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


class MemDock2(dict):
    def __init__(self):
        self.mask = []

    def set_mask(self, mask):
        self.mask = list(mask)
        self.mask.reverse()  # put least significant digit at index 0

    # I am 1000% sure I've made this harder than it needs to be.
    # Plus, doing this way has some pass-by-ref side-effects one has to be careful of
    def _get_all_floater_indicies(self, end_num, index_combos=[], start_num=0, result=[]):
        for n in range(start_num, end_num):
            self._get_all_floater_indicies(end_num, index_combos+[n], start_num=n+1, result=result)
            result.append(index_combos+[n])
        return result

    def __setitem__(self, key, val):
        d = {}
        float_positions = []
        for i,op in enumerate(self.mask):
            if op == '1':
                key = key | pow(2, i)
            if op == 'X':
                float_positions.append(pow(2, i))

        # Set all float positions to 0 so we know our start value for the bit position
        zeroed_floater_key = key
        for n in float_positions:
            if zeroed_floater_key & n:
                zeroed_floater_key -= n

        result = []
        d[zeroed_floater_key] = val
        floater_index_combos = self._get_all_floater_indicies(len(float_positions), result=result)
        for fic in floater_index_combos:
            float_val = 0
            for fi in fic:
                float_val+=float_positions[fi]

            d[zeroed_floater_key+float_val] = val

        self.update(d)


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
    md = MemDock2()
    for line in input:
        if line.startswith('mask'):
            md.set_mask(line.split()[-1])
        else:
            sl = line.split()
            key = int(sl[0].split('[')[-1][0:-1])
            val = int(sl[-1])
            md[key] = val

    print(sum(md.values()))


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
    #part1(input)
    part2(input)


if __name__ == '__main__':
    main()
