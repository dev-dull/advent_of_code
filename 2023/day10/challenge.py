import re
import argparse
from time import sleep


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
                'S': '╝'
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

    def traverse(self, animate=False):
        traveled_path_map = {
            '│': '║',
            '─': '═',
            '└': '╚',
            '┘': '╝',
            '┐': '╗',
            '┌': '╔',
            '.': '.',
            'S': 'S'
        }

        count = 1
        current_latitude = self.START[0] - 1
        current_longitude = self.START[1]
        came_from_latitude = self.START[0]
        came_from_longitude = self.START[1]
        while not (current_latitude == self.START[0] and current_longitude == self.START[1]):
            # self.pipe_land[current_latitude][current_longitude].printable = f"\033[1;32;40m{traveled_path_map[self.pipe_land[current_latitude][current_longitude].printable]}\033[0m"
            next_position_mod = self.pipe_land[current_latitude][current_longitude].get_next(came_from_latitude, came_from_longitude)
            came_from_latitude = current_latitude
            came_from_longitude = current_longitude
            current_latitude = next_position_mod[0]
            current_longitude = next_position_mod[1]
            count += 1
            if animate:
                self.pipe_land[came_from_latitude][came_from_longitude].printable = f"\033[1;32;40m{traveled_path_map[self.pipe_land[came_from_latitude][came_from_longitude].printable]}\033[0m"
                buff = '\033[2A' * len(self.pipe_land) + str(self)
                print(buff)
                sleep(0.01)
            else:
                self.pipe_land[came_from_latitude][came_from_longitude].printable = traveled_path_map[self.pipe_land[came_from_latitude][came_from_longitude].printable]

        return int(count/2)

    def __str__(self):
        visual = ''
        for line in self.pipe_land:
            for c in line:
                visual += str(c)
            visual += '\n'
        return visual


def part2(data):
    # .┌────┐┌┐┌┐┌┐┌─┐....
    # .│┌──┐││││││││┌┘....
    # .││.┌┘││││││││└┐....
    # ┌┘└┐└┐└┘└┘││└┘.└─┐..
    # └──┘.└┐...└┘S┐┌─┐└┐.
    # ....┌─┘..┌┐┌┘│└┐└┐└┐
    # ....└┐.┌┐││└┐│.└┐└┐│
    # .....│┌┘└┘│┌┘│┌┐│.└┘
    # ....┌┘└─┐.││.││││...
    # ....└───┘.└┘.└┘└┘...
    # Too high: 1064 - Copy/paste accident :-/
    # Too low:   378 - Educated guess, not a real try
    pipe_land = World14(data)
    pipe_land.traverse()
    inside = 0
    for ri, row in enumerate(pipe_land.pipe_land):
        for ci, column in enumerate(row):
            row_string = ''.join([str(r) for r in row])
            count = 0
            if row_string[ci] not in '║╚═╗╔╝':
                count = len(re.findall('║|╚[═]{0,}?╗|╔[═]{0,}?╝', row_string[ci:]))

            inside += count % 2

    print(inside)


def part1(data):
    pipe_land = World14(data)
    # Set 'animate' to True to animate the path following. On my machine, the animation runs for 9min.
    print(pipe_land.traverse(animate=False))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
