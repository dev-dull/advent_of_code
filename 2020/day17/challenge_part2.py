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
            retval[(w,h,0,0)] = lines[w][h] == '#'

    return retval,range(-1,width+1),range(-1,height+1),range(-1,2),range(-1,2)

def _make_ranges(keys):
    x = [i[0] for i in keys]
    y = [i[1] for i in keys]
    z = [i[2] for i in keys]
    w = [i[3] for i in keys]
    # range uses < logic to know when to end. +1 to adjust.
    xr = range(min(x), max(x)+1)
    yr = range(min(y), max(y)+1)
    zr = range(min(z), max(z)+1)
    wr = range(min(w), max(w)+1)
    return xr,yr,zr,wr

def _next_interval(input, x_range, y_range, z_range, w_range):
    # Note that defaultdict appears to create a copy of `input` for me, avoiding pass-by-ref issues.
    this_frame = defaultdict(lambda: False, input)
    next_frame = defaultdict(lambda: False, input)
    for w in w_range:
        for z in z_range:
            for x in x_range:
                for y in y_range:
                    neighbor_ct = 0
                    for cw in range(w-1, w+1+1):  # +1 for how range behaves, +1 again to check the neighboring area
                        for cz in range(z-1, z+1+1):
                            for cx in range(x-1, x+1+1):
                                for cy in range(y-1, y+1+1):
                                    if this_frame[(cx,cy,cz,cw)] and (cx,cy,cz,cw) != (x,y,z,w):
                                        neighbor_ct += 1

                    if this_frame[(x,y,z,w)] and neighbor_ct not in [2, 3]:
                        next_frame[(x,y,z,w)] = False
                    elif not this_frame[(x,y,z,w)] and neighbor_ct == 3:
                        next_frame[(x,y,z,w)] = True
                    else:
                        next_frame[(x,y,z,w)]

    # convert next_frame back to a dict to avoid indexing issues
    next_frame = dict(next_frame)
    # x, y, and z should've expanded in all directions (+ and -) by 1.
    return dict(next_frame),*_make_ranges(this_frame.keys())

def part2(input,x,y,z,w):
    for _ in range(0,6):
        input,x,y,z,w = _next_interval(input,x,y,z,w)

    print(len(list(filter(lambda t: t, input.values()))))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input,x,y,z,w = get_input(args.test)
    part2(input,x,y,z,w)


if __name__ == '__main__':
    main()
