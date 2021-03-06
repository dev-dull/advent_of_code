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
                return False
        return True

    def _nop(self, num):
        self.visited.append(self._index)

    def _acc(self, num):
        self.visited.append(self._index)
        self.acc += num

    def _jmp(self, num):
        self.visited.append(self._index)
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
    for i in range(0, len(input)):
        if input[i].startswith('nop'):
            oldop = 'nop'
            newop = 'jmp'
        elif input[i].startswith('jmp'):
            oldop = 'jmp'
            newop = 'nop'
        else:
            continue

        input[i] = input[i].replace(oldop, newop)
        gameboy = GameBoy(input)
        if gameboy.boot():
            print(gameboy.acc)
            break

        input[i] = input[i].replace(newop, oldop)


def part1(input):
    input.boot()
    print(input.acc)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    gameboy = GameBoy(input)
    #part1(gameboy)
    part2(input)


if __name__ == '__main__':
    main()
