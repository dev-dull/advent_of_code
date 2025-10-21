import argparse
from collections import defaultdict


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


class AntennaMap1(object):
    def __init__(self, antennaMap):
        self._antinodes = defaultdict(list)
        self.items = self._antinodes.items

        self.antennaMap = antennaMap
        self.rows = len(antennaMap)
        self.columns = len(antennaMap[0])

        self._antennaPositions = defaultdict(list)
        for y, line in enumerate(antennaMap):
            for x, c in enumerate(line):
                if c != '.':
                    self._antennaPositions[c].append((x, y))
        self._calculate_antinodes()

    def _calculate_antinodes(self):
        for frequency, coordinates in self._antennaPositions.items():
            for i, i_coordinate in enumerate(coordinates):
                for j_coordinate in coordinates[i+1:]:
                    coordinate_difference = (j_coordinate[0]-i_coordinate[0], j_coordinate[1]-i_coordinate[1])
                    antinode_candidates = []
                    for coordinate in [i_coordinate, j_coordinate]:
                        antinode_candidates.append((coordinate[0]-coordinate_difference[0], coordinate[1]-coordinate_difference[1]))
                        antinode_candidates.append((coordinate[0]+coordinate_difference[0], coordinate[1]+coordinate_difference[1]))
                    # Most of the logic of this `filter` call should be 'if' conditions, but this worked and I'm ready to move on.
                    self._antinodes[frequency] += list(filter(lambda an: an not in [i_coordinate, j_coordinate] and self.columns > an[0] >= 0 and self.rows > an[1] >=0 , antinode_candidates))

    def __str__(self):
        return '\n'.join(self.antennaMap)


class AntennaMap2(AntennaMap1):
    def _calculate_antinodes(self):
        for frequency, coordinates in self._antennaPositions.items():
            for i, i_coordinate in enumerate(coordinates):
                for j_coordinate in coordinates[i+1:]:
                    coordinate_difference = (j_coordinate[0]-i_coordinate[0], j_coordinate[1]-i_coordinate[1])
                    antinode_candidates = []
                    for coordinate in [i_coordinate, j_coordinate]:
                        # I should really make a list of modifiers (e.g. addition and subtraction) and loop over the list to make this more dry
                        # but this worked and I'm ready to move on to something else.
                        mult = 1
                        while self.columns > coordinate[0]-coordinate_difference[0]*mult >= 0 and self.rows > coordinate[1]-coordinate_difference[1]*mult >= 0:
                            c = (coordinate[0]-coordinate_difference[0]*mult, coordinate[1]-coordinate_difference[1]*mult)
                            antinode_candidates.append(c)
                            mult += 1

                        mult = 1
                        while self.columns > coordinate[0]+coordinate_difference[0]*mult >= 0 and self.rows > coordinate[1]+coordinate_difference[1]*mult >= 0:
                            c = (coordinate[0]+coordinate_difference[0]*mult, coordinate[1]+coordinate_difference[1]*mult)
                            antinode_candidates.append(c)
                            mult += 1

                    self._antinodes[frequency] += antinode_candidates


def part2(data):
    antennaMap = AntennaMap2(data)
    l = []
    for k, v in antennaMap.items():
        l += v
    print(len(set(l)))


def part1(data):
    antennaMap = AntennaMap1(data)
    l = []
    for k, v in antennaMap.items():
        l += v
    print(len(set(l)))


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
