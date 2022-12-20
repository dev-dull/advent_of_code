import json
import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        pairs = fin.read().split('\n\n')

    retval = []
    for pair in pairs:
        left, right = [json.loads(single) for single in pair.splitlines()]
        retval.append((left, right))

    return retval


def part2(data):
    pass


def part1(data):
    # Too low: 3594
    packet_index_sum = 0
    for i, pair in enumerate(data):
        if PacketOrderChecker(*pair):
            print('In order:')
            packet_index_sum += (i+1)
        else:
            print('Out of order:')
        print('\n'.join([str(pair[0]), str(pair[1])]), '\n\n')
    print(packet_index_sum)


class PacketOrderChecker(object):
    class _PacketPair(object):
        def __init__(self, value):
            self.value = value

        def __lt__(self, other):
            if isinstance(other.value, list) and not isinstance(self.value, list):
                return PacketOrderChecker._PacketPair([self.value]) < other
            elif isinstance(self.value, list) and not isinstance(other.value, list):
                return self < PacketOrderChecker._PacketPair([other.value])
            elif isinstance(self.value, int) and isinstance(other.value, int):
                return self.value < other.value
            elif isinstance(self.value, list) and isinstance(other.value, list):
                loop_max = min([len(self.value), len(other.value)])
                for i in range(0, loop_max):
                    if PacketOrderChecker._PacketPair(other.value[i]) < PacketOrderChecker._PacketPair(self.value[i]):
                        print(other.value[i], '<', self.value)
                        return False
                    elif PacketOrderChecker._PacketPair(self.value[i]) < PacketOrderChecker._PacketPair(other.value[i]):
                        return True
                # We made it out of the loop, fall back onto the length of the lists
                return len(self.value) < len(other.value)

            if self.value == [] and other.value != []:
                # self is an empty list, and therefore smaller than other
                # I first wrote this as `if not self.value and other.value` but zero will also eval to False.
                return True

            return self.value < other.value

        def __le__(self, other):
            return self.value < other.value or self.value == other.value

        def __gt__(self, other):
            return other.value < self.value

        def __ge__(self, other):
            return self.value > other.value or self.value == other

        def __eq__(self, other):
            return self.value == other.value

        def __ne__(self, other):
            return not self.value == other.value

    def __init__(self, left, right):
        self.left = self._PacketPair(left)
        self.right = self._PacketPair(right)

    def __bool__(self):
        return self.left < self.right


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)

    #part2(data)


if __name__ == '__main__':
    main()
