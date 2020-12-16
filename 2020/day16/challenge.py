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
        retval.append(list(line))
    return retval


class TicketValidator(dict):
    def __init__(self, ticket_rules):
        for ticket_rule in ticket_rules:
            rule_parts = ticket_rule.split(':')
            rule_ranges = rule_parts.split(' or ')

            rules = []
            for rule_range in rule_ranges:
                rule_range = [int(n) for n in rule_range.split('-')]
                rule_range[-1] += 1
                rules.append(lambda n: n in range(*rule_range))
            self[rule_parts[0]] = rules

    def validate(self, number):
        # I assume this is where the problem is going. I haven't finished reading it yet.
        for rule_name,rules in self.items():
            for rule in rules:
                if rule(number):
                    return True
        return False


def part2(input):
    pass


def part1(input):
    pass


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    #part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
