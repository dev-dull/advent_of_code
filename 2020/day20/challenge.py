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

    def refresh_sides(self, tile_name):
        row_ct = len([t[0] for t in self[tile_name]])
        _sides = []
        _sides.append(self[tile_name][0])  # Top
        _sides.append(self[tile_name][-1])  # Bottom
        _sides.append([self[tile_name][n][0] for n in range(0,row_ct)])  # This causes the left side to be backwards -_-
        _sides.append([self[tile_name][n][-1] for n in range(0,row_ct)])  # Right
        self.sides[tile_name] = _sides

    # Flip the tile horizontally
    def tile_hflip(self, tile_name):
        #if tile_name == 2393:
        #    print('before h-flip')
        #    for row in self[tile_name]:
        #        print(row)
        #    input('press enter...')


        flipped_tile = []
        for row in self[tile_name]:
            flipped_tile.append(copy(self[tile_name][-1::-1]))

        self[tile_name] = flipped_tile
        #if tile_name == 2393:
        #    print('after h-flip')
        #    for row in self[tile_name]:
        #        break
        #        print(row)

        self.refresh_sides(tile_name)


    # Rotate the tile turn_ct number of times
    def tile_rot(self, tile_name, turn_ct):
        row_ct = len([t[0] for t in self[tile_name]])
        for _ in range(0,turn_ct):
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

        for name_on_side,sides in self.sides.items():
            if name_on_side != tile_name:
                if side in sides:
                    return name_on_side,sides.index(side)
                elif rside in sides:
                    return name_on_side,sides.index(rside)

        return None,None  # We must've found the edge.

    def here_there_be_dragons(self):
        monster_hunter = '                  # #    ##    ##    ### #  #  #  #  #  #   '
        tile_order = []

        # Whichever tile is the first one I find that only has 2 matching sides gets to be the top-left corner.
        top_left_tile_name = None
        for tile_name,sides_ct in self.matching_sides_ct.items():
            if sides_ct == 2:
                top_left_tile_name = tile_name  # TODO: self.pop(tile_name), self.sides.pop(tile_name) ... etc
                break

        tile_order.append(top_left_tile_name)
        # figure out how the top left corner is positioned and rotate it as needed
        orientation = []
        for i,side in enumerate(self.sides[top_left_tile_name]):
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

        ## FIND all the tiles below the top-left tile and keep track of which tiles those are
        image_grid = []
        left_sides = []
        find_my_bottom = top_left_tile_name
        orientation = -1
        while find_my_bottom:
            # it is likely on the sweedish.
            previous_bottom =self[find_my_bottom][-1]
            left_sides.append(find_my_bottom)
            find_my_bottom,orientation = self.find_tile_to_side(find_my_bottom, self.BOTTOM)

            if orientation == self.RIGHT:
                self.tile_rot(find_my_bottom, 3)
            if orientation == self.BOTTOM:
                self.tile_rot(find_my_bottom, 2)
            if orientation == self.LEFT:
                self.tile_rot(find_my_bottom, 1)

        ## FIND all the tiles to the right of the left-edge tiles
        orientation = -1
        for ls in left_sides:
            image_grid.append([])
            find_my_right = ls
            old_right = None
            while find_my_right:
                if not old_right:
                    old_right = find_my_right
                    image_grid[-1].append(find_my_right)
                find_my_right,orientation = self.find_tile_to_side(find_my_right, self.RIGHT)

                if orientation == self.TOP:
                    self.tile_rot(find_my_right, 3)
                if orientation == self.RIGHT:
                    self.tile_rot(find_my_right, 2)
                if orientation == self.BOTTOM:
                    self.tile_rot(find_my_right, 1)

                # TODO: find the expected image width and remove the hard-coded 12
                if len(image_grid[-1])<12 and not find_my_right:
                    self.tile_hflip(old_right)
                    find_my_right = old_right
                    print(old_right)
                else:
                    old_right = None

        for row in image_grid:
            print(row)
        #for row in self[2393]:
        #    print('okay')
        #    print(row)

        #self.stitch_image(image_grid)

    def stitch_image(self, image_grid):
        image = []

        for image_row in image_grid:
            for tile_i in range(1,len(self[image_grid[0][0]])-1):
                try:
                    row = ''.join([''.join(self[tile_id][tile_i][1:-2]) for tile_id in image_row])
                    image.append(row)
                    #print(row)
                except Exception as e:
                    #print(image_row[tile_i])
                    #for row in self[image_row[tile_i]]:
                    #    print(row)
                    raise e

        #for i,_ in enumerate(self[image_grid[0]]):
        #    for tile_row in image_grid:
        #        self[tile_row][i]

        #for i,tile
        #    for tile_id in img_grid[i]:

        #for row_id in range(1,12-1):  # TODO: don't hard-code 12. Get the len() of the number of cols in an image block
        #    for img_block_id in image_grid:
        #        for img_row in self[img_block_id]:

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
