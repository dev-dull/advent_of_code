import yaml
import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        obj = yaml.load(fin.read().replace('  If ', 'If '), Loader=yaml.SafeLoader)

    return obj


def part2(data):
    # too high: 32390460700
    # too low:  20736431982

    lcm = 1
    monkeys = {}
    for monkey_id, monkey_stats in data.items():
        # Keep monkey_index a string, so I don't have to int() the ID of the monkey receiving an item.
        monkey_index = monkey_id.split()[-1]
        monkeys[monkey_index] = MonkeyP2(monkey_stats)
        lcm *= int(monkey_stats[MonkeyP2.C.TEST].split()[-1])

    # Oof. So many loops... room for improvement.

    # I was somewhat on the right track. I *might* have figured this out on my own given enough time, but
    # in the end, I looked up what other people did.
    # SUPER helpful explanation:
    # https://github.com/jonathanpaulson/AdventOfCode/blob/ecd9f556b7a8aa58350f35fe4346c6d1968402ba/2022/11.py#L28-L32
    # Injecting `lcm` into the object because ...... lazy ...
    for monkey_id, monkey in monkeys.items():
        monkey.lcm = lcm

    for _ in range(0, 10000):
        for monkey_id, monkey in monkeys.items():
            monkey(monkeys)

    monkey_businesses = []
    for monkey_id, monkey in monkeys.items():
        monkey_businesses.append(monkey.inspection_counter)
        print(f'Mokney {monkey_id}: {monkey}')
    monkey_businesses.sort(reverse=True)
    print(monkey_businesses[0] * monkey_businesses[1])


def part1(data):
    monkeys = {}
    for monkey_id, monkey_stats in data.items():
        # Keep monkey_index a string, so I don't have to int() the ID of the monkey receiving an item.
        monkey_index = monkey_id.split()[-1]
        monkeys[monkey_index] = Monkey(monkey_stats)

    for _ in range(0, 20):
        for monkey_id, monkey in monkeys.items():
            monkey(monkeys)

    monkey_businesses = []
    for monkey_id, monkey in monkeys.items():
        monkey_businesses.append(monkey.inspection_counter)
        print(f'Mokney {monkey_id}: {monkey}')
    monkey_businesses.sort(reverse=True)
    print(monkey_businesses[0] * monkey_businesses[1])


class Monkey(dict):
    class C(object):
        STARTING_ITEMS = 'Starting items'
        OPERATION = 'Operation'
        TEST = 'Test'
        IF_TRUE = 'If true'
        IF_FALSE = 'If false'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self[self.C.STARTING_ITEMS], int):
            # If the monkey is only starting with one item, then yaml loads it as an int.
            self[self.C.STARTING_ITEMS] = [self[self.C.STARTING_ITEMS]]
        else:
            # we got a string. Parse values to int
            self[self.C.STARTING_ITEMS] = [int(n) for n in self[self.C.STARTING_ITEMS].split(', ')]

        self._test = int(self[self.C.TEST].split()[-1])
        self._true_monkey = self[self.C.IF_TRUE].split()[-1]
        self._false_monkey = self[self.C.IF_FALSE].split()[-1]
        self.inspection_counter = 0

        self._antianxiety_factor = 3

    def __bool__(self):
        return not self[self.C.STARTING_ITEMS][0] % self._test

    def __call__(self, monkeys):
        while self[self.C.STARTING_ITEMS]:
            self._inspect()
            if self:
                appender = monkeys[self._true_monkey].append
            else:
                appender = monkeys[self._false_monkey].append
            appender(self[self.C.STARTING_ITEMS].pop(0))

    def __str__(self):
        return f'(inspected {self.inspection_counter}) ' + ', '.join(str(n) for n in self[self.C.STARTING_ITEMS])

    def _inspect(self):
        # I was hoping to find a simple solution that didn't use eval()
        # the `ast` library is built-in and looked somewhat simple, but I didn't want to spend a lot of time on it.
        # Instead, I'm going to build a new string that I 'trust' but I imagine `ast` would be the safer approach
        self.inspection_counter += 1
        trusted_string = ''
        anxiety_operation = self[self.C.OPERATION].split()
        for part in anxiety_operation:
            if part == 'old':
                trusted_string += str(self[self.C.STARTING_ITEMS][0])
            elif part in '+*':
                trusted_string += part
            elif part.isnumeric():
                trusted_string += part
        self[self.C.STARTING_ITEMS][0] = eval(trusted_string) // self._antianxiety_factor
        return trusted_string

    def append(self, anxiety_index):
        self[self.C.STARTING_ITEMS].append(anxiety_index)


class MonkeyP2(Monkey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._antianxiety_factor = 1

    def _inspect(self):
        trusted_string = super()._inspect()
        # As noted in part2(), I was on the right track, but it would've taken me forever to get here on my own.
        # SUPER helpful explanation:
        # https://github.com/jonathanpaulson/AdventOfCode/blob/ecd9f556b7a8aa58350f35fe4346c6d1968402ba/2022/11.py#L28-L32
        self[self.C.STARTING_ITEMS][0] = eval(trusted_string) % self.lcm

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
