import argparse

class Bags(dict):
    def __init__(self, input):
        for bag in input:
            self.add_bag(bag)

    def add_bag(self, raw_bag):
        this_bag_parts = raw_bag.split(' bags contain ')
        this_bag_name = this_bag_parts[0]

        self[this_bag_name] = {}  # If I were to do this over again, a bag would have pointers to the bags it can contain.
        if not this_bag_parts[1].startswith('no '):
            for raw_contents in this_bag_parts[1].split(', '):
                content_parts = raw_contents.split()
                self[this_bag_name][' '.join(content_parts[1:-1])] = int(content_parts[0])

    def holds_gold(self, color_name):
        if 'shiny gold' in self[color_name]:
            return True
        elif not self[color_name]:
            return False

        any_gold = []
        for color,ct in self[color_name].items():
            any_gold.append(self.holds_gold(color))
        return any(any_gold)

    def bag_count(self, color_name):
        count = []
        for color,ct in self[color_name].items():
            count.append(ct)
            for i in range(0,ct):
                count += self.bag_count(color)
        return count

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

    return lines


def part2(input):
    #input.bag_count('shiny gold')
    print(sum(input.bag_count('shiny gold')))


def part1(input):
    gold_ct = 0
    for color,contents in input.items():
        if input.holds_gold(color):
            gold_ct += 1
            #print(color)
    return gold_ct

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2020 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)

    bags = Bags(input)

    #import json
    #print(json.dumps(bags, indent=2))

    #print(part1(bags))
    part2(bags)


if __name__ == '__main__':
    main()
