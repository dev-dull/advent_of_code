import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        # Split the stack input from the move steps
        parts = fin.read().split('\n\n')

    return parts[0].splitlines(),parts[1].splitlines()


def part2(*input):
    supply_stack = SupplyStack9001(input[0])

    for step in input[1]:
        step_parts = step.split()
        # Indexing into a split string to get move info is gross, but I'm not thinking of a better alternative atm.
        supply_stack.do_stack_move(*[int(step_parts[1]), step_parts[3], step_parts[5]])

    supply_stack.print_top_of_stack()


def part1(*input):
    supply_stack = SupplyStack(input[0])

    for step in input[1]:
        step_parts = step.split()
        # Indexing into a split string to get move info is gross, but I'm not thinking of a better alternative atm.
        supply_stack.do_stack_move(*[int(step_parts[1]), step_parts[3], step_parts[5]])

    supply_stack.print_top_of_stack()


def poc_stack_parse(stack):
    # A proof-of-concept stack parse that should be able to handle >9 stacks
    # Only works if your IDE did not screw up input data by stripping trailing spaces
    # ...or if you know how to back-fill the 2d array with spaces.

    # import inside the method so we're not eating ram for POC work that will go unused
    import re
    import numpy

    np_stack = numpy.array([re.findall(' [0-9]+ |\[[A-Z]\]|    ', line) for line in stack])

    # I'm not too familiar with numpy, but it seems there's no rot270()  :-(
    np_stack = numpy.rot90(np_stack)
    np_stack = numpy.rot90(np_stack)
    np_stack = numpy.rot90(np_stack)

    h_stack = []
    for row in np_stack:
        if row[0][1].isnumeric():
            # I should probably use another regex here, but
            h_stack.append([re.sub('[ \[\]]', '', r) for r in row])

            # ew.
            while '' in h_stack[-1]:
                h_stack[-1].remove('')

    for hs in h_stack:
        print(hs)


class SupplyStack(object):
    def __init__(self, stack):
        stack.reverse()  # flip the stack vertically, so it's easier to loop over.
        column_positions = []
        self.columns = {}
        for pos, col_num in enumerate(stack[0]):
            # BUG: This'll break for > 9 columns
            if col_num.isnumeric():
                column_positions.append((pos, col_num))
                self.columns[col_num] = []

        for pos, col_num in column_positions:
            for stack_line in stack[1:]:
                # IDE stripped trailing spaces in input, causing 'IndexError: string index out of range' errors.
                if len(stack_line) >= pos and stack_line[pos] != ' ':
                    self.columns[col_num].append(stack_line[pos])

    def do_stack_move(self, num_to_move, from_stack, to_stack):
        for _ in range(0, num_to_move):
            c = self.columns[from_stack].pop()
            self.columns[to_stack].append(c)

    def print_top_of_stack(self):
        top_of_stack = ''
        for k, v in self.columns.items():
            top_of_stack += v[-1]
        print(top_of_stack)


class SupplyStack9001(SupplyStack):
    # Now with leather seats and A/C!!!
    def do_stack_move(self, num_to_move, from_stack, to_stack):
        # I almost did part 1 this way, with a `.reverse()` on the slice
        ni = num_to_move * -1
        self.columns[to_stack] += self.columns[from_stack][ni:]
        self.columns[from_stack] = self.columns[from_stack][0:ni]


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    # part1(*input)
    part2(*input)
    # poc_stack_parse(input[0])  # Thanks, me. I hate it.


if __name__ == '__main__':
    main()
