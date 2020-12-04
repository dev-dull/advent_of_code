def get_input():
    fin = open('input.list', 'r')
    lines = fin.read().splitlines()
    fin.close()

    while '' in lines:
        lines.remove('')

    retval = []
    for line in lines:
        retval.append(list(line))
    return retval


def part1(input, show_track=False):
    part2(input, 3, 1, show_track=show_track)


def part2(input, hslope, vslope, show_track=False):
    mod = len(input[0])
    hpos = 0
    treect = 0
    for ri in range(0,len(input),vslope):
        line=input[ri]
        if line[hpos%mod] == '#':
            treect += 1
            #line[hpos%mod] = 'X'
        #else:
            #line[hpos%mod] = 'O'

        hpos += hslope

        if show_track:
            print(''.join(line))

    return treect


def main():
    input = get_input()
    ##part1(input, show_track=True)
    trees_hit = []
    trees_hit.append(part2(input, 1, 1))
    trees_hit.append(part2(input, 3, 1))
    trees_hit.append(part2(input, 5, 1))
    trees_hit.append(part2(input, 7, 1))
    trees_hit.append(part2(input, 1, 2))
    from functools import reduce
    print('%s = %s' % (' * '.join([str(th) for th in trees_hit]), reduce(lambda a,b: a*b, trees_hit)))


if __name__ == '__main__':
    main()
