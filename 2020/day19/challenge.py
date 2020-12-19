import re
import argparse

def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')
    fin = open(fname, 'r')
    rules,lines = fin.read().split('\n\n')
    fin.close()

    srules = rules.splitlines()
    data = lines.splitlines()

    rules = {}
    for rule in srules:
        rule_id,rule_parts = rule.split(': ')
        if '"' in rule_parts:  # Just to reduce the amount we're "Lost In Silly Parens"
            rule_parts = rule_parts.replace('"', '')
        else:
            rule_parts = '( %s )' % ')|('.join(rule_parts.split('|'))
        rule_parts = rule_parts.split(' ')
        rules[rule_id] = rule_parts
    return rules,data

def part2(input):
    pass


def part1(rules, data):
    updating = True
    while updating:
        updating = False
        for k,v in rules.items():
            for i,c in enumerate(v):
                if c in rules:
                    rules[k] = v[:i] + ['('] + rules[c] + [')'] + v[i+1:]
                    updating = True

    matches = 0
    for line in data:
        if re.fullmatch(''.join(rules['0']), line):
            matches += 1
            print(line)
    print(matches)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    rules,data = get_input(args.test)
    part1(rules, data)
    #part2(input)


if __name__ == '__main__':
    main()
