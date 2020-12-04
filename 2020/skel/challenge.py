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


def part2(input):
    pass


def part1(input):
    pass


def main():
    input = get_input()
    #part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
