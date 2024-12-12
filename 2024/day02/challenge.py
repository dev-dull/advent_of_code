import argparse

class Building(list):
    class _Floor(list):
        def __init__(self, rooms):
            super().__init__()
            for room in rooms.split():
                self.append(int(room))

        @property
        def increasing(self):
            return self[0] - self[-1] < 0

        @property
        def decreasing(self):
            return self[0] - self[-1] > 0

        @property
        def safe(self):
            for i in range(len(self)-1):
                if not self.increasing and not self.decreasing:
                    # first minus last is zero
                    return False
                if abs(self[i]-self[i+1]) > 3:
                    # too big of a change
                    return False
                if self.increasing and self[i]-self[i+1] > 0:
                    # first minus last detected increasing, but adjecent numbers decrease
                    return False
                if self.decreasing and self[i]-self[i+1] < 0:
                    # first minus last detected decreasing, but adjecent numbers increase
                    return False
                if not self[i]-self[i+1]:
                    # same number (difference of zero)
                    return False
            return True

    def __init__(self, floors):
        super().__init__()
        for floor in floors:
            self.append(self._Floor(floor))


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


def part2(data):
    pass


def part1(data):
    building = Building(data)
    safety = ''
    safety_count = 0
    for floor in building:
        if floor.safe:
            safety = 'Safe'
            safety_count += 1
        else:
            safety = 'Unsafe'
        print(floor, safety)
    print(safety_count)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
