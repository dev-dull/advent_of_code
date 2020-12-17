import argparse
from collections import defaultdict

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

    width = len(lines[0])
    height = len(lines)
    retval = {}  # Learning my lesson from day15 and using a dict (instead of a 3D array) to speed things up.
    for h in range(0,height):
        for w in range(0,width):
            retval[(w,h,0)] = lines[w][h] == '#'

    return retval,range(-1,width+1),range(-1,height+1),range(-1,2)

def _make_ranges(keys):
    x = [i[0] for i in keys]
    y = [i[1] for i in keys]
    z = [i[2] for i in keys]
    # range uses < logic to know when to end. +1 to adjust.
    xr = range(min(x), max(x)+1)
    yr = range(min(y), max(y)+1)
    zr = range(min(z), max(z)+1)
    return xr,yr,zr

def _next_interval(input, x_range, y_range, z_range):
    # Note that defaultdict appears to create a copy of `input` for me, avoiding pass-by-ref issues.
    this_frame = defaultdict(lambda: False, input)
    next_frame = defaultdict(lambda: False, input)
    for z in z_range:
        for x in x_range:
            for y in y_range:
                neighbor_ct = 0
                for cz in range(z-1, z+1+1):  # +1 for how range behaves, +1 again to check the neighboring area
                    for cx in range(x-1, x+1+1):
                        for cy in range(y-1, y+1+1):
                            if this_frame[(cx,cy,cz)] and (cx,cy,cz) != (x,y,z):
                                neighbor_ct += 1

                if this_frame[(x,y,z)] and neighbor_ct not in [2, 3]:
                    next_frame[(x,y,z)] = False
                elif not this_frame[(x,y,z)] and neighbor_ct == 3:
                    next_frame[(x,y,z)] = True
                else:
                    next_frame[(x,y,z)]

    # convert next_frame back to a dict to avoid indexing issues
    next_frame = dict(next_frame)
    # x, y, and z should've expanded in all directions (+ and -) by 1.
    return dict(next_frame),*_make_ranges(this_frame.keys())

def print_energy_pocket(input, x_range, y_range, z_range):
    for z in z_range:
        print('Z = %s' % z)
        for x in x_range:
            for y in y_range:
                print('#' if (x,y,z) in input and input[(x,y,z)] else '.', end='')
            print('')
        print('')


def part2(input):
    pass


def part1(input,x,y,z):
    for _ in range(0,6):
        input,x,y,z = _next_interval(input,x,y,z)

    print(len(list(filter(lambda t: t, input.values()))))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input,x,y,z = get_input(args.test)
    part1(input,x,y,z)
    #part2(input)


if __name__ == '__main__':
    main()
