import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


class _Part1(object):
    def __init__(self, values, previous):
        self.value = values[0]
        self.multiply = self.value * previous
        self.add = self.value + previous

        self.next_add = None
        self.next_multiply = None
        if values[1:]:
            self.next_add = _Part1(values[1:], self.add)
            self.next_multiply = _Part1(values[1:], self.multiply)

    def __eq__(self, value):
        if self.next_add:
            return self.next_add == value or self.next_multiply == value
        return value in [self.add, self.multiply]


class Part1(object):
    def __init__(self, total, values):
        self.total = total
        self.values_tree = _Part1(values[1:], values[0])

    def __bool__(self):
        return self.values_tree == self.total


def _make_data_p1(data):
    clean_data = []
    for d in data:
        total, str_values = d.split(': ')
        values = str_values.split()
        clean_data.append((int(total), [int(v) for v in values]))
    return clean_data


def part1(raw_data):
    x = 0
    data = _make_data_p1(raw_data)
    for total, values in data:
        p1 = Part1(total, values)
        if p1:
            x += total
    print(x)


class _Part2(_Part1):
    def __init__(self, values, previous):
        # Using super().__init__ will cause `next_add` and `next_multiply` to be of type `_Part1` not `_Part2`
        self.value = values[0]
        self.multiply = self.value * previous
        self.add = self.value + previous
        self.concat = int(f"{previous}{self.value}")

        self.next_add = None
        self.next_multiply = None
        self.next_concat = None
        if values[1:]:
            self.next_add = _Part2(values[1:], self.add)
            self.next_multiply = _Part2(values[1:], self.multiply)
            self.next_concat = _Part2(values[1:], self.concat)

    def __eq__(self, value):
        if self.next_add:
            return super().__eq__(value) or self.next_concat == value
        return value in [self.add, self.multiply, self.concat]


class Part2(Part1):
    def __init__(self, total, values):
        self.total = total
        self.values_tree = _Part2(values[1:], values[0])


def part2(raw_data):
    x = 0
    data = _make_data_p1(raw_data)
    for total, values in data:
        p2 = Part2(total, values)
        if p2:
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
