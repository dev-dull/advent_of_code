import argparse


class PlantMapping(dict):
    def __setitem__(self, starts, _range):
        destination_start = starts[0]
        source_start = starts[1]
        super().__setitem__(range(source_start, source_start+_range),
                    (destination_start, _range))

    def __getitem__(self, item):
        for item_range in self:
            if item in item_range:
                destination_start, _range = super().__getitem__(item_range)
                x = item - item_range[0]
                return x+destination_start
        return item

def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        parts = fin.read().strip().split('\n\n')

    seeds = [int(s) for s in parts[0].split(': ')[-1].split()]

    almanac_info = {}
    for category in parts[1:]:
        category_lines = category.splitlines()
        category_name = category_lines[0].split(' map:')[0]
        almanac_info[category_name] = PlantMapping()
        for category_line in category_lines[1:]:
            mappings = [int(v) for v in category_line.split()]
            almanac_info[category_name][(mappings[0], mappings[1])] = mappings[2]

    return seeds, almanac_info


def part2(data):
    pass


def part1(seeds, almanac_info):
    locations = []
    for seed in seeds:
        seedling = seed
        for mapping in almanac_info.values():
            seedling = mapping[seedling]
        locations.append(seedling)
    print(min(locations))



def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    seeds, almanac_info = get_input(args.test)
    part1(seeds, almanac_info)
    #part2(data)


if __name__ == '__main__':
    main()
