import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


# wonk-wonk-wonk -- It's Mario in that pipe. We're chasing Mario.
class World14(object):
    class _pipe_segment(object):
        def __init__(self, segment, latitude, longitude):
            super().__init__()
            self.latitude = latitude
            self.longitude = longitude

            self.printable = {
                '|': '│',
                '-': '─',
                'L': '└',
                'J': '┘',
                '7': '┐',
                'F': '┌',
                '.': '.',
                'S': 'S'
            }[segment]

            # came_from - current
            # │ :
            #   (0, 3) - (1, 3) = (-1, 0)
            #   (2, 3) - (1, 3) = (1, 0)
            # ─ :
            #   (3, 3) - (3, 2) = (0, 1)
            #   (3, 1) - (3, 2) = (0, -1)
            # └ :
            #   (3, 0) - (4, 0) = (-1, 0)
            #   (4, 1) - (4, 0) = (0, 1)
            # ┘ :
            #   (2, 0) - (2, 1) = (0, -1)
            #   (1, 1) - (2, 1) = (-1, 0)
            # ┐ :
            #   (0, 2) - (0, 3) = (0, -1)
            #   (1, 3) - (0, 3) = (1, 0)
            # ┌ :
            #   (1, 2) - (0, 2) = (1, 0)
            #   (0, 3) - (0, 2) = (0, 1)
            # ..┌┐.
            # .┌┘│.
            # ┌┘.└┐
            # │┌──┘
            # └┘...
            self.come_and_go_map = {
                '|': ((-1, 0), (1, 0)),
                '-': ((0, 1), (0, -1)),
                'L': ((-1, 0), (0, 1)),
                'J': ((0, -1), (-1, 0)),
                '7': ((0, -1), (1, 0)),
                'F': ((0, 1), (1, 0)),
                '.': None,
                'S': ((0, 0),)
            }[segment]

        def get_next(self, came_from_latitude, came_from_longitude):
            next_mod_i = self.come_and_go_map.index((came_from_latitude - self.latitude, came_from_longitude - self.longitude)) - 1
            return (self.latitude + self.come_and_go_map[next_mod_i][0], self.longitude + self.come_and_go_map[next_mod_i][1])

        def __str__(self):
            return self.printable

    def __init__(self, pipe_land):
        self.pipe_land = []
        self.START = tuple()
        for latitude, line in enumerate(pipe_land):
            self.pipe_land.append([])
            for longitude, pipe in enumerate(line):
                if pipe == 'S':
                    self.START = (latitude, longitude)
                self.pipe_land[-1].append(self._pipe_segment(pipe, latitude, longitude))

    def traverse(self):
        count = 1
        current_latitude = self.START[0] - 1
        current_longitude = self.START[1]
        came_from_latitude = self.START[0]
        came_from_longitude = self.START[1]
        while not (current_latitude == self.START[0] and current_longitude == self.START[1]):
            next_position_mod = self.pipe_land[current_latitude][current_longitude].get_next(came_from_latitude, came_from_longitude)
            came_from_latitude = current_latitude
            came_from_longitude = current_longitude
            current_latitude = next_position_mod[0]
            current_longitude = next_position_mod[1]
            count += 1
        print(int(count/2))

    def __str__(self):
        visual = ''
        for line in self.pipe_land:
            for c in line:
                visual += str(c)
            visual += '\n'
        return visual


def part2(data):
    pass


def part1(data):
    pipe_land = World14(data)
    # print(pipe_land)
    pipe_land.traverse()


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
