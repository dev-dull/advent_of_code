import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        grid = fin.read().strip().split('\n\n')

    return [g.splitlines() for g in grid]


def part2(data):
    pass


def rotate(grid):
    rot_grid = []
    for ci, _ in enumerate(grid[0]):
        new_row = []
        for ri, __ in enumerate(grid):
            # (c+1)*-1 creates negative index to work backwards. Without this, we mirror in addition to rotate.
            new_row.append(grid[ri][(ci+1)*-1])
        rot_grid.append(''.join(new_row))
    return rot_grid


def find_reflection_intersection(mirror_grid):
    for i, row in enumerate(mirror_grid[0:-1]):
        if mirror_grid[i] == mirror_grid[i + 1]:
            sub_side = i - 1
            add_side = i + 2
            mirrored = True
            while sub_side+1 and len(mirror_grid) - add_side:
                if mirror_grid[sub_side] == mirror_grid[add_side]:
                    sub_side -= 1
                    add_side += 1
                else:
                    mirrored = False
                    break

            if mirrored:
                return i, i + 1


def part1(data):
    # Too high: 30584 - I was indexing into reflection_points incorrectly
    # Too high: 30541 - I failed to use rot_grid when adding up the totals in the else statement
    total = 0
    for mirror_grid in data:
        reflection_points = find_reflection_intersection(mirror_grid)
        if reflection_points:
            total += len(mirror_grid[0:reflection_points[0]+1])*100
        else:
            rot_grid = rotate(mirror_grid)
            reflection_points = find_reflection_intersection(rot_grid)
            total += len(rot_grid[reflection_points[1]:])
    print(total)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
