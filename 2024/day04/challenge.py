import argparse


class WordSearch(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.start_locations = []
        self.xmas_locations = []
        self.row_count = len(self)
        self.col_count = len(self[0])

        self._WORD = 'XMAS'
        self._WORD_LENGTH = len(self._WORD)

        self._find_all_starts()

    def _find_all_starts(self):
        for r, line in enumerate(self):
            search_position = 0
            try:
                while True:
                    c = line.index(self._WORD[0], search_position)
                    self.start_locations.append((r, c))
                    search_position = c + 1
            except ValueError:
                # Using an error to break out of a loop has always felt like a bad plan, but I'm
                # assuming the '.index()' method is more efficient than any search I would write in python.
                continue

    def _search_left_right(self, r, c):
        # check left to right
        if c + self._WORD_LENGTH - 1 < self.col_count:
            return self._WORD == ''.join([self[r][cc] for cc in range(c, c + self._WORD_LENGTH)])
        return False

    def _search_right_left(self, r, c):
        # check right to left
        if c - (self._WORD_LENGTH - 1) > -1:
            return self._WORD == ''.join([self[r][cc] for cc in range(c, c - self._WORD_LENGTH, -1)])
        return False

    def _search_top_down(self, r, c):
        # check top down
        if r + self._WORD_LENGTH - 1 < self.row_count:
            return self._WORD == ''.join([self[rr][c] for rr in range(r, r + self._WORD_LENGTH)])
        return False

    def _search_bottom_up(self, r, c):
        # check bottom up
        if r - (self._WORD_LENGTH - 1) > -1:
            return self._WORD == ''.join([self[rr][c] for rr in range(r, r - self._WORD_LENGTH, -1)])
        return False

    def _search_up_right(self, r, c):
        # check up and right (r-1, c+1)
        if r - (self._WORD_LENGTH - 1) > -1 and c + self._WORD_LENGTH - 1 < self.col_count:
            positions = map(lambda rr, cc: (rr, cc), range(r, r - self._WORD_LENGTH, -1), range(c, c + self._WORD_LENGTH))
            return self._WORD == ''.join([self[rr][cc] for rr, cc in positions])
        return False

    def _search_up_left(self, r, c):
        # check up and left (r-1, c-1)
        if r - (self._WORD_LENGTH - 1) > -1 and c - (self._WORD_LENGTH - 1) > -1:
            positions = map(lambda rr, cc: (rr, cc), range(r, r - self._WORD_LENGTH, -1), range(c, c - self._WORD_LENGTH, -1))
            return self._WORD == ''.join([self[rr][cc] for rr, cc in positions])
        return False

    def _search_down_right(self, r, c):
        # check down and right (r+1, c+1)
        if r + self._WORD_LENGTH - 1 < self.row_count and c + self._WORD_LENGTH - 1 < self.col_count:
            positions = map(lambda rr, cc: (rr, cc), range(r, r + self._WORD_LENGTH), range(c, c + self._WORD_LENGTH))
            return self._WORD == ''.join([self[rr][cc] for rr, cc in positions])
        return False

    def _search_down_left(self, r, c):
        # check down and left (r+1, c-1)
        if r + self._WORD_LENGTH - 1 < self.row_count and c - (self._WORD_LENGTH - 1) > -1:
            positions = map(lambda rr, cc: (rr, cc), range(r, r + self._WORD_LENGTH), range(c, c - self._WORD_LENGTH, -1))
            return self._WORD == ''.join([self[rr][cc] for rr, cc in positions])
        return False

    def search(self):
        tests = [
            self._search_left_right,
            self._search_right_left,
            self._search_top_down,
            self._search_bottom_up,
            self._search_up_right,
            self._search_up_left,
            self._search_down_right,
            self._search_down_left
        ]
        for r, c in self.start_locations:
            test_results = [test(r, c) for test in tests]
            [self.xmas_locations.append((r, c)) for tr in filter(lambda b: b, test_results)]

        return self.xmas_locations


class XMasSearch(WordSearch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_locations = []
        self._WORD = 'MAS'
        self._WORD_LENGTH = len(self._WORD)
        self._find_all_starts()

    def search(self):
        for r, c in self.start_locations:
            if self._search_down_right(r, c):
                if self._search_up_right(r+2, c) or self._search_down_left(r, c+2):
                    self.xmas_locations.append((r, c))

            if self._search_up_right(r, c):
                if self._search_down_right(r-2, c) or self._search_up_left(r, c+2):
                    self.xmas_locations.append((r, c))

            if self._search_up_left(r, c):
                if self._search_up_right(r, c-2) or self._search_down_left(r-2, c):
                    self.xmas_locations.append((r, c))

            if self._search_down_left(r, c):
                if self._search_down_right(r, c-2) or self._search_up_left(r+2, c):
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
    xmas_search = XMasSearch(data)
    print(int(len(xmas_search.search())/2))


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