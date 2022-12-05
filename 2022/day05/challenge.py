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


def part2(input):
    pass


def part1(*input):
    supply_stack = SupplyStack(input[0])

    for step in input[1]:
        step_parts = step.split()
        # Indexing into a split string to get move info is gross, but I'm not thinking of a better alternative atm.
        supply_stack.do_stack_move(*[int(step_parts[1]), step_parts[3], step_parts[5]])

    top_of_stack = ''
    for k, v in supply_stack.columns.items():
        top_of_stack += v[-1]
    print(top_of_stack)


class SupplyStack(object):
    def __init__(self, stack):
        stack.reverse()  # flip the stack vertically, so it's easier to loop over.
        column_positions = []
        self.columns = {}
        for pos, col_num in enumerate(stack[0]):
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


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    part1(*input)
    #part2(input)


if __name__ == '__main__':
    main()
