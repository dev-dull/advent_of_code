import argparse
from collections import defaultdict

def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    lines = fin.read().split('\n\n')
    fin.close()

    return lines

class image_blocks(dict):
    def __init__(self, raw_image_data):
        self.matching_sides_ct = defaultdict(lambda: 0)
        self.sides = {}

        for image_data in raw_image_data:
            image_lines = image_data.splitlines()
            tile_name = int(image_lines[0].split()[-1][:-1])
            self[tile_name] = [list(il) for il in image_lines[1:]]

            _sides = []
            img_height = len(self[tile_name])

            _sides.append(self[tile_name][0])  # Top
            _sides.append(self[tile_name][-1])  # Bottom
            _sides.append([self[tile_name][n][0] for n in range(0,img_height)])  # Left
            _sides.append([self[tile_name][n][-1] for n in range(0,img_height)])  # Right
            self.sides[tile_name] = _sides

        import json
        for tile_name,_sides in self.sides.items():
            other_tile_sides = []
            for other_name,other_sides in self.sides.items():
                if tile_name != other_name:
                    other_tile_sides += other_sides

            for side in _sides:
                if side in other_tile_sides:
                    self.matching_sides_ct[tile_name] += 1
                else:
                    side.reverse()
                    if side in other_tile_sides:
                        self.matching_sides_ct[tile_name] += 1

def part2(input):
    pass


def part1(input):
    result = 1
    for tile_id,matching_sides_ct in input.matching_sides_ct.items():
        if matching_sides_ct == 2:
            result *= tile_id
    print(result)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    images = image_blocks(get_input(args.test))

    part1(images)
    #part2(input)


if __name__ == '__main__':
    main()
