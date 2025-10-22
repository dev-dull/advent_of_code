import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip()

    return lines


class AmphipodFS(object):
    def __init__(self, compressed_disk_map):
        self._blocks_moved = 0
        self.disk_map = []
        for i, c in enumerate(compressed_disk_map):
            if i % 2:
                self.disk_map += ["."] * int(c)
            else:
                self.disk_map += [int(i/2)] * int(c)

    def defragment(self):
        # Input gets tricky by making it so that a "." ends up in the last position, so skip self.disk_map[-1] in the check
        while "." in self.disk_map[0:-1]:
            i = self.disk_map.index(".")
            n = self.disk_map.pop()
            self.disk_map[i] = n
            self._blocks_moved += 1

    def AmP5(self):
        checksum = 0
        for i, id in enumerate(self.disk_map):
            # Input gets tricky by making it so that a "." ends up in the last position, so test for condition
            if id != ".":
                checksum += i * id
        return checksum

    def __str__(self):
        return ''.join([str(c)[0] for c in self.disk_map] + ["."] * self._blocks_moved)



def part2(data):
    pass


def part1(data):
    fs = AmphipodFS(data)
    fs.defragment()
    print(fs.AmP5())


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2024 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    parser.add_argument('-2', '--part2', dest='part2', action='store_true', default=False, help='Run part 2 instead of part 1')
    args = parser.parse_args()
    data = get_input(args.test)

    f = part2 if args.part2 else part1
    f(data)


if __name__ == '__main__':
    main()
