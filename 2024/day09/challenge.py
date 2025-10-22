import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip()

    return lines


class AmphipodFS1(object):
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


class AmphipodFS2(AmphipodFS1):
    def _get_last_file(self, end_position):
        for i in range(end_position-1, -1, -1):
            if self.disk_map[i] != ".":
                # Question: is the built-in `[].index()` faster than continuing to search backwards?
                # Because we care about the _end_ of the list, it would have to be tested. If faster, uncomment
                # the next line and remove dead code.
                # return self.disk_map.index(self.disk_map[i]), i+1
                j = i
                while self.disk_map[j] == self.disk_map[i]:
                    j -= 1
                # `j+1` since we'll step back one time too many
                # `i+1` since `"string"[j:i]` omits the `i` position (`<` and not `<=`)
                return j+1, i+1
        return None

    def _find_free_space(self, required_size):
        # It's a little hacky to use the string to find the free space, but because we care about space closer
        # to the _start_, I expect that Python's built-in `"".index()` is faster than anything I would write here.
        size_string = "." * required_size
        str_map = str(self)
        if size_string in str_map:
            return str_map.index(size_string)
        return None

    def defragment(self):
        end_position = len(self.disk_map)
        while end_position > 0:
            sof, eof = self._get_last_file(end_position)
            free = self._find_free_space(eof-sof)
            if free and free < sof:
                for free_i, data_i in zip(range(free, free+(eof-sof)), range(sof, eof)):
                    self.disk_map[free_i] = self.disk_map[data_i]
                    self.disk_map[data_i] = "."

            end_position = sof


def part2(data):
    fs = AmphipodFS2(data)
    fs.defragment()
    print(fs.AmP5())


def part1(data):
    fs = AmphipodFS1(data)
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
