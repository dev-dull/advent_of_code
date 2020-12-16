import argparse
from copy import deepcopy

def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    parts = fin.read().split('\n\n')
    fin.close()

    while '' in parts:
        parts.remove('')

    rules = parts[0].splitlines()
    my_ticket = [int(n) for n in parts[1].splitlines()[-1].split(',')]
    nearby_tickets = []
    for line in parts[2].splitlines()[1:]:
        nearby_tickets.append([int(n) for n in line.split(',')])

    return rules,my_ticket,nearby_tickets


class TicketValidator(dict):
    def __init__(self, ticket_rules):
        for ticket_rule in ticket_rules:
            rule_parts = ticket_rule.split(': ')
            rule_ranges = rule_parts[1].split(' or ')

            valid_ranges = []
            for rule_range in rule_ranges:
                rule_range = [int(n) for n in rule_range.split('-')]
                rule_range[-1] += 1
                # I thought I'd be clever by appending the validation function itself
                # But this caused all kinds of pass-by-ref headaches
                #valid_ranges.append(lambda n: n in range(*rule_range))
                valid_ranges.append(rule_range)
            self[rule_parts[0]] = valid_ranges

    def validate(self, numbers):
        invalid_numbers = []
        for number in numbers:
            is_valid = False
            for rule_name,valid_ranges in self.items():
                for valid_range in valid_ranges:
                    is_valid = number in range(*valid_range)
                    if is_valid:
                        break
                if is_valid:
                    break
            if not is_valid:
                invalid_numbers.append(number)
        return invalid_numbers

def part2(input):
    pass


def part1(rules, my_ticket, nearby_tickets):
    validator = TicketValidator(rules)
    invalid = []
    for nearby_ticket in nearby_tickets:
        invalid += validator.validate(nearby_ticket)

    print(sum(invalid))

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    rules,my_ticket,nearby_tickets = get_input(args.test)
    part1(rules, my_ticket, nearby_tickets)
    #part2(input)


if __name__ == '__main__':
    main()
