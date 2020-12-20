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
            rule_parts = '( %s )' % ') | ('.join(rule_parts.split('|'))
        rule_parts = rule_parts.split(' ')
        rules[rule_id] = rule_parts
    return rules,data


def part2(rules, data):
    # new plan: filter down to all the rule numbers != the recursive one
    # each rule number becomes '(rn)+' where rn is the rule number.
    while any([r.isnumeric() for r in rules['0']]):
        for k,v in rules.items():
            for i,c in enumerate(v):
                if c in rules:
                    if c == k:  # Recursion!!!
                        rule_parts_index = v.index('|')
                        recursion_index = v.index(c)
                        rule_part_a = v[:rule_parts_index]
                        rule_part_b = v[rule_parts_index+1:]
                        if c in rule_part_a:
                            rules[k] = v[:recursion_index] + ['('] + rule_part_b + [')', '+'] + v[recursion_index+1:]
                        else:
                            rules[k] = v[:recursion_index] + ['('] + rule_part_a + [')', '+'] + v[recursion_index+1:]
                        #print(''.join(rules[k]))
                        #return
                    rules[k] = v[:i] + ['('] + rules[c] + [')'] + v[i+1:]

    matches = 0
    for line in data:
        if re.fullmatch(''.join(rules['0']), line):
            matches += 1
            print(line)
    #print(''.join(rules['0']))
    print(matches)  # 369 is the answer -- I found it by guessing. 



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
    #part1(rules, data)
    part2(rules, data)


if __name__ == '__main__':
    main()
