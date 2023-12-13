import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


# For part 1
class CosmicExpansion(object):
    def __init__(self, starfield):
        # They're supposed to be galaxies, not stars, but I've already committed to the naming
        self.starfield = self._expand_universe(starfield)
        self.starpoints = self._find_stars()

    def _expand_universe(self, starfield, expansion_factor=1):
        empty_columns = []
        for ci, _ in enumerate(starfield[0]):
            if len(set([r[ci] for r in starfield])) == 1:
                empty_columns.append(ci)

        empty_rows = []
        for ri, row in enumerate(starfield):
            if len(set(row)) == 1:
                empty_rows.append(ri)

        empty_row = '.' * len(starfield[0])
        empty_rows.reverse()  # work backwards so that we don't screw up our line indicies for every new row added
        for ri in empty_rows:
            for _ in range(0, expansion_factor):
                starfield = starfield[:ri] + [empty_row] + starfield[ri:]

        empty_columns.reverse()
        for ci in empty_columns:
            for ri, row in enumerate(starfield):
                for _ in range(0, expansion_factor):
                    starfield[ri] = starfield[ri][:ci] + '.' + starfield[ri][ci:]

        return starfield

    def measure_distance(self, star1, star2):
        return (abs(star1[0] - star2[0]) + abs(star1[1] - star2[1]))

    def _find_stars(self):
        starpoints = []
        for ri, row in enumerate(self.starfield):
            for ci, point in enumerate(row):
                if point == '#':
                    starpoints.append((ri, ci))
        return starpoints


# For part 2
class MathyCosmicExpansion(CosmicExpansion):
    def __init__(self, starfield):
        self.starfield = starfield
        self.starpoints = self._find_stars()

    def _find_expansions(self):
        empty_columns = []
        for ci, _ in enumerate(self.starfield[0]):
            if len(set([r[ci] for r in self.starfield])) == 1:
                empty_columns.append(ci)

        empty_rows = []
        for ri, row in enumerate(self.starfield):
            if len(set(row)) == 1:
                empty_rows.append(ri)

        return empty_rows, empty_columns

    def _find_stars(self):
        empty_rows, empty_columns = self._find_expansions()
        starpoints = []
        row_offset = 0
        for ri, row in enumerate(self.starfield):
            column_offset = 0
            if ri in empty_rows:
                row_offset += 999999

            for ci, point in enumerate(row):
                if ci in empty_columns:
                    column_offset += 999999

                if point == '#':
                    starpoints.append((ri+row_offset, ci+column_offset))
        return starpoints


def part2(data):
    # Too High: 622121608984 - knowing full well I have a bug (offsets of 10 and 100 were both 82 too high, so I subtracted 82)
    # Too low:      82000210 - Ran with the -t flag and wasted an attempt
    ce = MathyCosmicExpansion(data)
    star_distances = []
    for spi1, sp1 in enumerate(ce.starpoints):
        for sp2 in ce.starpoints[spi1 + 1:]:
            star_distances.append(ce.measure_distance(sp1, sp2))
    print(sum(star_distances))


def part1(data):
    # Using a class really didn't offer much value on this one.
    ce = CosmicExpansion(data)
    star_distances = []
    for spi1, sp1 in enumerate(ce.starpoints):
        for sp2 in ce.starpoints[spi1+1:]:
            star_distances.append(ce.measure_distance(sp1, sp2))
    print(sum(star_distances))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
