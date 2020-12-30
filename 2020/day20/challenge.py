import re
import argparse
from copy import copy
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
        self.TOP    = 0
        self.BOTTOM = 1
        self.LEFT   = 2
        self.RIGHT  = 3

        self.matching_sides_ct = defaultdict(lambda: 0)
        self.sides = {}

        for image_data in raw_image_data:
            image_lines = image_data.splitlines()
            tile_name = int(image_lines[0].split()[-1][:-1])
            self[tile_name] = [list(il) for il in image_lines[1:]]

            _sides = []
            img_height = len(self[tile_name])

            self.refresh_sides(tile_name)

        for tile_name,_sides in self.sides.items():
            other_tile_sides = []
            for other_name,other_sides in self.sides.items():
                if tile_name != other_name:
                    other_tile_sides += other_sides

            for side in _sides:
                if side in other_tile_sides:
                    self.matching_sides_ct[tile_name] += 1
                    side_index = other_tile_sides.index(side)
                else:
                    side.reverse()
                    if side in other_tile_sides:
                        self.matching_sides_ct[tile_name] += 1
                        side_index = other_tile_sides.index(side)
                    side.reverse()  # flip it back for later.

    # Update the cache that contains just the tile sides
    def refresh_sides(self, tile_name):
        row_ct = len([t[0] for t in self[tile_name]])
        _sides = []
        _sides.append(self[tile_name][0])  # Top
        _sides.append(self[tile_name][-1])  # Bottom
        # _sides.append([self[tile_name][n][0] for n in range(row_ct-1, -1, -1)])  # count down so side is in expected order
        _sides.append([self[tile_name][n][0] for n in range(0, row_ct)])  # This causes the left side to be backwards, but for how sides are compared, this ends up giving the expected results.
        _sides.append([self[tile_name][n][-1] for n in range(0, row_ct)])  # Right
        self.sides[tile_name] = _sides

    # Flip the tile horizontally
    def tile_hflip(self, tile_name):
        flipped_tile = []
        for row in self[tile_name]:
            flipped_tile.append(row[-1::-1])

        self[tile_name] = flipped_tile
        self.refresh_sides(tile_name)

    # Rotate the tile turn_ct number of times
    def tile_rot(self, tile_name, turn_ct):
        row_ct = len([t[0] for t in self[tile_name]])
        for _ in range(0, turn_ct):
            rotated_tile = []
            for rn in range(0, row_ct):
                new_row = [t[rn] for t in self[tile_name][-1::-1]]
                rotated_tile.append(new_row)
            self[tile_name] = copy(rotated_tile)

        self.refresh_sides(tile_name)

    def find_tile_to_side(self, tile_name, find_side):
        side = self.sides[tile_name][find_side]
        rside = copy(side)
        rside.reverse()

        for name_on_side, sides in self.sides.items():
            if name_on_side != tile_name:
                if side in sides:
                    return name_on_side, sides.index(side)
                elif rside in sides:
                    return name_on_side, sides.index(rside)

        return None, None  # We must've found the edge.

    def here_there_be_dragons(self):
        tile_order = []

        # Whichever tile is the first one I find that only has 2 matching sides gets to be the top-left corner.
        top_left_tile_name = None
        for tile_name, sides_ct in self.matching_sides_ct.items():
            if sides_ct == 2:
                top_left_tile_name = tile_name  # TODO: self.pop(tile_name), self.sides.pop(tile_name) ... etc
                break

        tile_order.append(top_left_tile_name)
        # figure out how the top left corner is positioned and rotate it as needed
        orientation = []
        for i, side in enumerate(self.sides[top_left_tile_name]):
            rside = copy(side)
            rside.reverse()
            for tile_name,sides in self.sides.items():
                if top_left_tile_name != tile_name:
                    if (side in sides) or (rside in sides):
                        orientation.append(i)

        if self.LEFT in orientation and self.BOTTOM in orientation:
            self.tile_rot(top_left_tile_name, 3)
        elif self.LEFT in orientation and self.TOP in orientation:
            self.tile_rot(top_left_tile_name, 2)
        elif self.RIGHT in orientation and self.TOP in orientation:
            self.tile_rot(top_left_tile_name, 1)

        # FIND all the tiles below the top-left tile and keep track of which tiles those are
        image_grid = []
        left_sides = []
        find_my_bottom = top_left_tile_name
        orientation = -1
        while find_my_bottom:
            # it is likely on the sweedish.
            previous_bottom = self.sides[find_my_bottom][self.BOTTOM]
            left_sides.append(find_my_bottom)
            find_my_bottom, orientation = self.find_tile_to_side(find_my_bottom, self.BOTTOM)

            if orientation == self.RIGHT:
                self.tile_rot(find_my_bottom, 3)
            if orientation == self.BOTTOM:
                self.tile_rot(find_my_bottom, 2)
            if orientation == self.LEFT:
                self.tile_rot(find_my_bottom, 1)

            if find_my_bottom and self.sides[find_my_bottom][self.TOP] == previous_bottom[-1::-1]:
                self.tile_hflip(find_my_bottom)

        # FIND all the tiles to the right of the left-edge tiles
        orientation = -1
        for ri, ls in enumerate(left_sides):
            image_grid.append([])
            find_my_right = ls
            ci = -1
            while find_my_right:
                ci += 1
                image_grid[-1].append(find_my_right)
                previous_right = self.sides[find_my_right][self.RIGHT]
                find_my_right, orientation = self.find_tile_to_side(find_my_right, self.RIGHT)

                if orientation == self.TOP:
                    self.tile_rot(find_my_right, 3)
                if orientation == self.RIGHT:
                    self.tile_rot(find_my_right, 2)
                if orientation == self.BOTTOM:
                    self.tile_rot(find_my_right, 1)

                # TODO: it should be possible to determine if we need to hflip before any other rotations
                if find_my_right and self.sides[find_my_right][self.LEFT] == previous_right[-1::-1]:
                    # print('needed hflip+rotate:', find_my_right)
                    self.tile_hflip(find_my_right)
                    self.tile_rot(find_my_right, 2)

        for row in image_grid:
            print('r', row)

        images = self.stitch_image(image_grid)
        # TODO: Items in `monster` only match an 'image' the size of the test data.
        # monster_hunter = list('                  # #    ##    ##    ### #  #  #  #  #  #   '.replace(' ', '.'))


        # monster_hunter = list('#    ##    ##    ###'.replace(' ', '.'))
        # retnuh_retsnom = copy(monster_hunter)
        # retnuh_retsnom.reverse()
        # monsters = [''.join(monster_hunter), ''.join(retnuh_retsnom)]

        monster_head   = re.compile('..................#.')
        monster_middle = re.compile('#....##....##....###')
        monster_bottom = re.compile('.#..#..#..#..#..#...')

        # monster_head   = re.compile('.#..................')
        # monster_middle = re.compile('###....##....##....#')
        # monster_bottom = re.compile('...#..#..#..#..#..#.')

        monster_ct = 0
        for ri, line in enumerate(images[1]):
            # print('L', line)
            if 0 < ri < len(images[1]):
                for match in monster_middle.finditer(line):
                    print('matched middle', ri)
                    if monster_head.search(images[1][ri+1][match.start():match.end()]):  # if ri+1 on this line, then checking for upsidedown monster.
                        print('matched head', ri)
                        if monster_bottom.search(images[1][ri-1][match.start():match.end()]):  # if ri-1 on this line, then checking for upsidedown monster.
                            print('matched bottom', ri)
                            monster_ct += 1

        # The original plan was to loop through all the characters in monster_hunter and all the characters in the image
        # and match test `monster_c == ' ' or (ord(monster_c) ^ ord(image_c) == 0)` but using regex is faster
        # monster_ct = re.findall(monsters[1], images[1])  # 0,1 0,0 1,0
        print('counted N monsters:', monster_ct)
        # print(monsters)
        print('turbulence:', ''.join(images[1]).count('#'))

    def stitch_image(self, image_grid):
        # My image is 96 rows (correct) by 84 cols (incorrect) suggesting that my [1:-2 is in the wrong place]
        image = []
        for image_row in image_grid:
            for tile_i in range(1, len(self[image_grid[0][0]])-1):
                row = ''.join([''.join(self[tile_id][tile_i][1:-1]) for tile_id in image_row])
                image.append(row)
                # print('ALD', row)

        # Rotate the grid
        self['temp'] = image_grid
        self.tile_rot('temp', 1)  # Hijack my existing code
        image_grid = self.pop('temp')

        # Rotate the individual tiles so everything lines up as expected
        for tile_row in image_grid:
            for tile_name in tile_row:
                self.tile_rot(tile_name, 1)

        # Build the rotated image and hope there isn't some pass-by-ref nonsense going with how `image` was built.
        rot_image = []
        for image_row in image_grid:
            for tile_i in range(1, len(self[image_grid[0][0]])-1):
                row = ''.join([''.join(self[tile_id][tile_i][1:-1]) for tile_id in image_row])
                rot_image.append(row)
                # print(row)

        for image_row in image_grid:
            print('')
            for tile_i in range(0, len(self[image_grid[0][0]])):
                print(' '.join([''.join(self[tile_id][tile_i]) for tile_id in image_row]))

        unwound = ''.join(image)
        rot_unwound = ''.join(rot_image)
        # print(len(unwound), len(rot_unwound))
        # for row in image:
        #     print('return', row)
        # print('WTF', rot_image)
        return image, rot_image
        # return unwound, rot_unwound
        # print(unwound)
        # for monster in monsters:
        #     # TODO: loop through characters and True if space or # in monster matches # in image
        #     print(monster)


def part2(input):
    input.here_there_be_dragons()


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
    part2(images)


if __name__ == '__main__':
    main()
