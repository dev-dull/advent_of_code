import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip()
    rules, pages = lines.split('\n\n')

    return rules, pages


class PrintRules(dict):
    def __init__(self, rules, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for rule in rules.splitlines():
            self._add_rule(rule)

    def _add_rule(self, rule):
        k, v = rule.split('|')
        if k in self:
            self[k].append(v)
        else:
            self[k] = [v]

    def __eq__(self, pages):
        for i, page in enumerate(pages):
            if page in self:
                for rule in self[page]:
                    if rule in pages[:i]:
                        return False
        return True


def part2(rules, pages):
    pass


def part1(rules, pages):
    pretty_mid = []
    print_rules = PrintRules(rules)
    for page in pages.splitlines():
        print_list = page.split(',')
        if print_rules == print_list:
            pretty_mid.append(print_list[int(len(print_list)/2)])
    print(sum([int(n) for n in pretty_mid]))


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2024 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    parser.add_argument('-2', '--part2', dest='part2', action='store_true', default=False, help='Run part 2 instead of part 1')
    args = parser.parse_args()
    rules, pages = get_input(args.test)

    f = part2 if args.part2 else part1
    f(rules, pages)


if __name__ == '__main__':
    main()
