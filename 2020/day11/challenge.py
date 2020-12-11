import argparse
from copy import deepcopy

class Seat(str):
    EMPTY = 'L'
    OCCUPIED = '#'

    # I'm not yet sure which of these will be the most useful, so just making them all while I'm here
    occupied = lambda self: self == '#'
    open_seat = lambda self: self == 'L'
    sro = lambda self: self == '.'  # Standing room only

class Seats(list):
    def __init__(self, row):
        for seat in row:
            self.append(Seat(seat))

    def occupied_count(self):
        return self.count('#')


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    lines = fin.read().splitlines()
    fin.close()

    while '' in lines:
        lines.remove('')

    return [Seats(l) for l in lines]


def part2(input):
    pass


def _part1(input):
    next_seating = deepcopy(input)
    made_change = False
    for r,row in enumerate(input):
        for c,col in enumerate(row):
            # build a list of neighbor seats we care to check
            # This is ugly, but far more readable than the other options I was considering
            if col.sro():
                continue

            occupied_neighbor_ct = 0
            if r-1 >= 0:
                occupied_neighbor_ct += 1 if input[r-1][c].occupied() else 0
                if c-1 >= 0:
                    occupied_neighbor_ct += 1 if input[r-1][c-1].occupied() else 0
                if c+1 < len(row):
                    occupied_neighbor_ct += 1 if input[r-1][c+1].occupied() else 0
            if c-1 >= 0:
                occupied_neighbor_ct += 1 if input[r][c-1].occupied() else 0
            if c+1 < len(row):
                occupied_neighbor_ct += 1 if input[r][c+1].occupied() else 0
            if r+1 < len(input):
                occupied_neighbor_ct += 1 if input[r+1][c].occupied() else 0
                if c-1 >= 0:
                    occupied_neighbor_ct += 1 if input[r+1][c-1].occupied() else 0
                if c+1 < len(row):
                    occupied_neighbor_ct += 1 if input[r+1][c+1].occupied() else 0

            #print(r,c)
            if input[r][c].occupied() and occupied_neighbor_ct > 3:
                next_seating[r][c] = Seat(Seat.EMPTY)
                made_change = True
            elif input[r][c].open_seat() and occupied_neighbor_ct == 0:
                next_seating[r][c] = Seat(Seat.OCCUPIED)
                made_change = True
            #else:
            #    print(r, c, input[r][c], occupied_neighbor_ct)

    return next_seating,made_change

def part1(input):
    changes = True
    while changes:
        input,changes = _part1(input)

    print(sum(map(lambda r: r.occupied_count(), input)))

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
