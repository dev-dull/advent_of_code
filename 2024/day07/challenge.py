import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


def _make_data_p1(data):
    clean_data = []
    for d in data:
        total, str_values = d.split(': ')
        values = str_values.split()
        clean_data.append((int(total), [int(v) for v in values]))
    return clean_data

class _BridgeCalibrator(object):
    def __init__(self, values, previous, modifiers):
        self.value = values[0]
        self.modified_values = [m(self.value, previous) for m in modifiers]
        self.next_values = [_BridgeCalibrator(values[1:], mv, modifiers) for mv in self.modified_values] if values[1:] else [None]

    def __eq__(self, value):
        if self.next_values[0]:
            return any([n == value for n in self.next_values])
        return value in self.modified_values


class BridgeCalibrator(object):
    def __init__(self, total, values, modifiers):
        self.total = total
        self._bc = _BridgeCalibrator(values[1:], values[0], modifiers)

    def __bool__(self):
        return self._bc == self.total


def part2(raw_data):
    modifiers = [
        lambda v, p: v * p,
        lambda v, p: v + p,
        lambda v, p: int(f"{p}{v}"),
    ]
    data = _make_data_p1(raw_data)
    x = 0
    for total, values in data:
        p1 = BridgeCalibrator(total, values, modifiers)
        if p1:
            x += total
    print(x)


def part1(raw_data):
    modifiers = [
        lambda v, p: v * p,
        lambda v, p: v + p,
    ]
    data = _make_data_p1(raw_data)
    x = 0
    for total, values in data:
        p1 = BridgeCalibrator(total, values, modifiers)
        if p1:
            x += total
    print(x)


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
