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

    retval = []
    for line in lines:
        retval.append([int(n) for n in line.split(',')])
    return retval


def part2(input):
    part1(input, 30000000)  # clearly there's some math thing that'll get me to the answer faster, but /me gestures at my job. I'll just let this run.


def elf_game(has_been_spoken):
    ct = len(has_been_spoken)+1
    last_spoken_at  = list(range(1,ct))  # The turn number when the number in the parallel array was last spoken
    speak = has_been_spoken[-1]
    next_up = 0

    while True:
        yield (speak,ct)
        speak = next_up
        if next_up in has_been_spoken:
            i = has_been_spoken.index(next_up)
            next_up = ct - last_spoken_at[i]
            last_spoken_at[i] = ct
        else:
            has_been_spoken.append(speak)
            last_spoken_at.append(ct)
            next_up = 0

        ct += 1

def part1(input, end_at):
    eg = elf_game(input)
    ct = 0
    while ct < end_at+1:
        spoken,ct = next(eg)
    print(spoken, ct)

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()

    input = get_input(args.test)
    for l in input:
        #part1(l, 2020)
        part2(input)


if __name__ == '__main__':
    main()
