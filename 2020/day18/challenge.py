import argparse

def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    lines = fin.read().splitlines()
    fin.close()

    retvals = []
    for line in lines:
        # strip out the spaces
        line = ''.join(line.split())

        # It appears that they only give me single digit numbers
        # but I feel like pushing myself to handle numbers 2 or more digits long
        # and I don't want to resort to using regex ... because why keep things simple?
        i=0
        new_line = []  # This a *new line* not a *newline* (i.e. \n)
        while i < len(line):
            if line[i] in '()+*':
                new_line.append(line[i])
                i+=1
            else:
                new_line.append('')
                while i < len(line) and line[i].isnumeric():
                    new_line[-1] += line[i]
                    i+=1

        # convert numbers from str to int
        new_line = [int(nl) if nl.isnumeric() else nl for nl in new_line]

        retvals.append(new_line)

    return retvals


def part2(input):
    pass


def _eqs(eq):
    return ''.join([str(e) for e in eq])

def bad_math(eq, depth=0):
    open_paren_index = 0
    total = 0
    while '(' in eq:
        open_paren_index = eq.index('(')
        close_paren_index = 0
        paren_ct = 0
        for i,c in enumerate(eq[open_paren_index+1:]):
            if c == '(':
                paren_ct += 1
            elif c == ')' and paren_ct == 0:
                close_paren_index = i + open_paren_index + 1
                break
            elif c == ')':
                paren_ct -= 1

        total = bad_math(eq[open_paren_index+1:close_paren_index], depth=depth+1)
        eq = eq[:open_paren_index] + [total] + eq[close_paren_index+1:]

    total = 0
    i = 0
    while ('*' in eq) or ('+' in eq):
        if eq[i] == '+':
            total = eq[i-1] + eq[i+1]
            eq = eq[:i-1] + [total] + eq[i+2:]
            i = len(eq[:i-1] + [total])
        elif eq[i] == '*':
            total = eq[i-1] * eq[i+1]
            eq = eq[:i-1] + [total] + eq[i+2:]
            i = len(eq[:i-1] + [total])
        else:
            i += 1

    return total


def part1(input):
    results = []
    for line in input:
        results.append(bad_math(line))

    print(sum(results))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
