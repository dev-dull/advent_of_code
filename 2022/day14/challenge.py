import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    retval = []
    for line in lines:
        pairs = []
        for pair in line.split(' -> '):
            if pair:
                a, b = pair.split(',')
                pairs.append((int(a), int(b)))
        if pairs:
            retval.append(pairs)

    return retval


def part2(data):
    pass


def part1(data):
    cave = Cavern(data)
    print(cave.bottom_edge)
    print(cave, '\n')
    counts = 0

    while cave():
        counts += 1

    print(cave)
    print(counts)


class Cavern(object):
    class Rock(object):
        def __str__(self):
            return '#'

    class Sand(object):
        def __str__(self):
            return 'o'

    def __init__(self, ddd_scan_data):
        self.cavern_model = {}
        self.left_edge = float('inf')
        self.right_edge = 0
        self.bottom_edge = 0

        for line in ddd_scan_data:
            prev_pos = [-1, -1]
            for pos in line:
                # Find the edges as we render the cave
                if pos[0] < self.left_edge:
                    self.left_edge = pos[0]
                if pos[0] > self.right_edge:
                    self.right_edge = pos[0]
                if pos[1] > self.bottom_edge:
                    self.bottom_edge = pos[1]

                # Don't try to draw anything yet if we're starting a new line
                if prev_pos[0] >= 0 <= prev_pos[1]:
                    index = None
                    for i, v in enumerate(pos):
                        # find the index of the value that changed from previous
                        if v != prev_pos[i]:
                            index = i
                            break
                    xedni = abs(index - 1)  # compute the index of the value that didn't change

                    # set the start/end values for range()
                    ranger = [prev_pos[index], pos[index]]
                    ranger.sort()
                    ranger[-1] += 1

                    # draw/set the cave wall
                    for point_value in range(*ranger):
                        point = [None, None]
                        point[index] = point_value
                        point[xedni] = pos[xedni]
                        self.cavern_model[tuple(point)] = self.Rock()
                prev_pos = pos

    def __call__(self, deep_hurting=(500, 0)):
        '''
        :param deep_hurting: I couldn't resist the MST3K reference here.
        :return: bool on if the sand fell off the edge of the world.
        '''
        while True:
            not_in_freefall = deep_hurting[1] <= self.bottom_edge
            if (deep_hurting[0], deep_hurting[1]+1) not in self.cavern_model and not_in_freefall:
                # Down
                deep_hurting = (deep_hurting[0], deep_hurting[1]+1)
            elif (deep_hurting[0]-1, deep_hurting[1]+1) not in self.cavern_model and not_in_freefall:
                # Down and left
                deep_hurting = (deep_hurting[0]-1, deep_hurting[1]+1)
            elif (deep_hurting[0]+1, deep_hurting[1]+1) not in self.cavern_model and not_in_freefall:
                # Down and right
                deep_hurting = (deep_hurting[0]+1, deep_hurting[1]+1)
            elif not_in_freefall:
                self.cavern_model[deep_hurting] = self.Sand()
                return True
            else:
                return False

    def __str__(self):
        retval = ''
        for row in range(0, self.bottom_edge+1):
            for col in range(self.left_edge, self.right_edge+1):
                if (col, row) in self.cavern_model:
                    retval += str(self.cavern_model[(col, row)])
                else:
                    retval += '.'
            retval += '\n'
        return retval



def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)

    #part2(data)


if __name__ == '__main__':
    main()
