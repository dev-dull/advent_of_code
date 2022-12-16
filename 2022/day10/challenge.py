import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    return lines


def part2(data):
    pass


def part1(data):
    picture = RGBPhotonGunCyclotron()
    for d in data:
        picture(*d.split())
    print(picture[220])  # just in case they rudely give me input long enough to hit 260.


class RGBPhotonGunCyclotron(object):
    def __init__(self):
        self.value = 1
        self.cycle_interval = self._cycle_intervals()
        self.cycle_target = next(self.cycle_interval)
        self._cycles_elapsed = 0
        self.operations = {
            'noop': self.noop,
            'addx': self.addx
        }
        self.intervals = {}

    def _cycle_intervals(self):
        c = 20
        while True:
            yield c
            c += 40

    def __call__(self, *args):
        # Playing around with strategies that let the library user treat the input as code without doing spooky things
        # like using `eval()` and `getattr()`
        if args:
            # luckily, a slice of an empty array (e.g. `[][1:]`) just results in an empty array.
            # This lets me gracefully pass nothing to `noop()` and my int to `addx()`
            self.operations[args[0]](*args[1:])

    def __next__(self):
        self._cycles_elapsed += 1
        if self._cycles_elapsed == self.cycle_target:
            # print(f'{self.cycle_target}*{self.value}={self.cycle_target*self.value}')
            self.intervals[self.cycle_target] = self.value
            self.cycle_target = next(self.cycle_interval)

    def __getitem__(self, value):
        signals = []
        for k, v in self.intervals.items():
            if k <= value:
                signals.append(k*v)
        return sum(signals)

    def noop(self):
        next(self)

    def addx(self, value):
        self.noop()
        self.noop()
        self.value += int(value)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
