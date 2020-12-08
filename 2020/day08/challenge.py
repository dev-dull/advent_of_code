import argparse
from functools import partial


class GameBoy(list):
    def __init__(self, operations):
        self.acc = 0
        self._index = 0
        self.visited = []
        for op in operations:
            parts = op.split()
            func = eval('self._'+parts[0])  # Always 'eval' your input data from strangers........
            self.append(partial(func, int(parts[1])))

    def boot(self):
        while self._index < len(self):
            self[self._index]()
            self._index += 1
            if self._index in self.visited:
                #print('Index %s already visted. Bailing out' % str(self._index+1))
                #print([i+1 for i in self.visited])
                break

    def _nop(self, num):
        self.visited.append(self._index)
        #print('nop')

    def _acc(self, num):
        self.visited.append(self._index)
        #print('acc')
        self.acc += num

    def _jmp(self, num):
        self.visited.append(self._index)
        #print('jmp')
        self._index += num
        self._index -= 1  # We're about to +1 back in boot()


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


def part2(input):
    pass


def part1(input):
    input.boot()
    print(input.acc)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    gameboy = GameBoy(input)
    part1(gameboy)
    #part2(input)


if __name__ == '__main__':
    main()
