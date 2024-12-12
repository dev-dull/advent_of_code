import re
import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip()

    return lines


# here's a bad plan that'll work
# like, seriously, never, EVER blindly eval() strings you don't trust
def mul(a, b):
    return int(a) * int(b)


def part2(data):
    do_mult = True
    calculations = []
    mul_exp = re.compile('mul\([0-9]{1,},[0-9]{1,}\)|((do|don\'t)\(\))')
    for me in mul_exp.finditer(data):
        operation = me.group()
        if operation.startswith('do'):
            do_mult = (operation == 'do()')

        if do_mult and operation.startswith('mul('):
            calculations.append(operation)

    # here's a bad plan that'll work
    # like, seriously, never, EVER blindly eval() strings you don't trust
    print(sum([eval(c) for c in calculations]))


def part1(data):
    mul_exp = re.compile('mul\([0-9]{1,},[0-9]{1,}\)')

    # here's a bad plan that'll work
    # like, seriously, never, EVER blindly eval() strings you don't trust
    results = [eval(match.group()) for match in mul_exp.finditer(data)]
    print(sum(results))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2024 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
