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

    def identify_fields(self, number):
        possible_fields = []
        for rule_name,valid_ranges in self.items():
            is_valid = False
            for valid_range in valid_ranges:
                is_valid = number in range(*valid_range)
                if is_valid:
                    break
            if is_valid:
                possible_fields.append(rule_name)
        return possible_fields

def part2(rules, my_ticket, nearby_tickets):
    my_ticket = [int(n) for n in my_ticket]
    nearby_tickets.append(my_ticket)
    validator = TicketValidator(rules)
    valid_tickets = []
    for nearby_ticket in nearby_tickets:
        if not validator.validate(nearby_ticket):
            valid_tickets.append(nearby_ticket)

    possible_fields_map = {}
    for i in range(0,len(valid_tickets[0])):
        possible_fields_map[i] = list(validator.keys())

    for numbers in valid_tickets:
        for i,number in enumerate(numbers):
            possible_fields = validator.identify_fields(number)
            for possible_field in possible_fields_map[i]:
                if possible_field not in possible_fields:
                    possible_fields_map[i].remove(possible_field)

    while list(filter(lambda n: len(n)>1, possible_fields_map.values())):
        known_field_positions = {}
        for position,field_name in possible_fields_map.items():
            if len(field_name) == 1:
                known_field_positions[position] = field_name

        for known_position,known_field_name in known_field_positions.items():
            for position,field_names in possible_fields_map.items():
                if known_position != position:
                    if known_field_name[0] in field_names:
                        possible_fields_map[position].remove(known_field_name[0])

    departure_multi = 1
    for position,name in possible_fields_map.items():
        if name[0].startswith('departure'):
            departure_multi *= my_ticket[position]
    print(departure_multi)


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
    #part1(rules, my_ticket, nearby_tickets)
    part2(rules, my_ticket, nearby_tickets)


if __name__ == '__main__':
    main()
