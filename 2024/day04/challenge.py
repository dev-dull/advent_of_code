import argparse


class WordSearch(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.x_locations = []
        self.xmas_locations = []
        self.row_count = len(self)
        self.col_count = len(self[0])

        self._WORD = 'XMAS'
        self._WORD_LENGTH = len(self._WORD)

        self._find_all_x()

    def _find_all_x(self):
        for r, line in enumerate(self):
            search_position = 0
            try:
                while True:
                    c = line.index('X', search_position)
                    self.x_locations.append((r, c))
                    search_position = c + 1
            except ValueError:
                # Using an error to break out of a loop has always felt like a bad plan, but I'm
                # assuming the '.index()' method is more efficient than any search I would write in python.
                continue

    def search(self):
        for r, c in self.x_locations:
            # check left to right
            if c + self._WORD_LENGTH - 1 < self.col_count:
                if self._WORD == ''.join([self[r][cc] for cc in range(c, c+self._WORD_LENGTH)]):
                    self.xmas_locations.append((r, c))

            # check right to left
            if c - (self._WORD_LENGTH - 1) > -1:
                if self._WORD == ''.join([self[r][cc] for cc in range(c, c - self._WORD_LENGTH, -1)]):
                    self.xmas_locations.append((r, c))

            # check top down
            if r + self._WORD_LENGTH - 1 < self.row_count:
                if self._WORD == ''.join([self[rr][c] for rr in range(r, r + self._WORD_LENGTH)]):
                    self.xmas_locations.append((r, c))

            # check bottom up
            if r - (self._WORD_LENGTH - 1) > -1:
                if self._WORD == ''.join([self[rr][c] for rr in range(r, r - self._WORD_LENGTH, -1)]):
                    self.xmas_locations.append((r, c))

            # check up and right (r-1, c+1)
            if r - (self._WORD_LENGTH - 1) > -1 and c + self._WORD_LENGTH - 1 < self.col_count:
                positions = map(lambda rr, cc: (rr, cc), range(r, r - self._WORD_LENGTH, -1), range(c, c + self._WORD_LENGTH))
                if self._WORD == ''.join([self[rr][cc] for rr, cc in positions]):
                    self.xmas_locations.append((r, c))

            # check up and left (r-1, c-1)
            if r - (self._WORD_LENGTH - 1) > -1 and c - (self._WORD_LENGTH - 1) > -1:
                positions = map(lambda rr, cc: (rr, cc), range(r, r - self._WORD_LENGTH, -1), range(c, c - self._WORD_LENGTH, -1))
                if self._WORD == ''.join([self[rr][cc] for rr, cc in positions]):
                    self.xmas_locations.append((r, c))

            # check down and right (r+1, c+1)
            if r + self._WORD_LENGTH - 1 < self.row_count and c + self._WORD_LENGTH - 1 < self.col_count:
                positions = map(lambda rr, cc: (rr, cc), range(r, r + self._WORD_LENGTH), range(c, c + self._WORD_LENGTH))
                if self._WORD == ''.join([self[rr][cc] for rr, cc in positions]):
                    self.xmas_locations.append((r, c))

            # check down and left (r+1, c-1)
            if r + self._WORD_LENGTH - 1 < self.row_count and c - (self._WORD_LENGTH - 1) > -1:
                positions = map(lambda rr, cc: (rr, cc), range(r, r + self._WORD_LENGTH), range(c, c - self._WORD_LENGTH, -1))
                if self._WORD == ''.join([self[rr][cc] for rr, cc in positions]):
                    self.xmas_locations.append((r, c))

        return self.xmas_locations


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


def part2(data):
    pass


def part1(data):
    word_search = WordSearch(data)
    print(len(word_search.search()))


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
