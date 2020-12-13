import argparse

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

    return lines

class Navigate(dict):
    def __init__(self):
        self.EAST = 0
        self.SOUTH = 90
        self.WEST = 180
        self.NORTH = 270

        self.direction = self.EAST
        self[self.EAST] = 0
        self[self.SOUTH] = 0
        self[self.WEST] = 0
        self[self.NORTH] = 0

    def navigate(self, input):
        for line in input:
            func = eval('self.'+line[0])
            func(int(line[1:]))

        return abs(self[self.EAST] - self[self.WEST]),abs(self[self.NORTH] - self[self.SOUTH])

    def N(self, distance):
        self[self.NORTH] += distance

    def S(self, distance):
        self[self.SOUTH] += distance

    def E(self, distance):
        self[self.EAST] += distance

    def W(self, distance):
        self[self.WEST] += distance

    def L(self, degrees):
        self.direction = (self.direction - degrees) % 360

    def R(self, degrees):
        self.direction = (self.direction + degrees) % 360

    def F(self, distance):
        self[self.direction] += distance


class Navigate2(object):
    def __init__(self):
        self.wp_x = 10  # waypoint x and y
        self.wp_y = 1

        self.pos_x = 0
        self.pos_y = 0

    def navigate(self, input):
        for line in input:
            func = eval('self.'+line[0])
            func(int(line[1:]))

        return abs(self.pos_x),abs(self.pos_y)
        #return abs(self[self.EAST] - self[self.WEST]),abs(self[self.NORTH] - self[self.SOUTH])

    def N(self, distance):
        self.wp_y += distance

    def S(self, distance):
        self.wp_y -= distance

    def E(self, distance):
        self.wp_x += distance

    def W(self, distance):
        self.wp_x -= distance

    def L(self, degrees):
        # swap x and y, then x*=-1
        for _ in range(0, degrees, 90):
            tmp = self.wp_x
            self.wp_x = self.wp_y * -1
            self.wp_y = tmp

    def R(self, degrees):
        # swap x and y, then y*=-1
        for _ in range(0, degrees, 90):
            tmp = self.wp_x * -1
            self.wp_x = self.wp_y
            self.wp_y = tmp

    def F(self, distance):
        self.pos_x = self.pos_x + (self.wp_x * distance)
        self.pos_y = self.pos_y + (self.wp_y * distance)

def part2(input):
    n=Navigate2()
    ew,ns = n.navigate(input)

    print('%s + %s = %s' % (ew, ns, ew+ns))


def part1(input):
    n=Navigate()
    ew,ns = n.navigate(input)

    print('%s + %s = %s' % (ew, ns, ew+ns))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    #part1(input)
    part2(input)


if __name__ == '__main__':
    main()
