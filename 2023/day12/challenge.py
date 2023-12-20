import argparse
from re import sub


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    data = []
    for line in lines:
        parts = line.split()
        #                     Operational        Damaged
        key = parts[0].replace('.', 'o').replace('#', 'D')
        data.append((key, [int(n) for n in parts[1].split(',')]))

    return data


def get_all_spring_strings(spring_string, strings):
    if '?' in spring_string:
        spring_string_parts = list(spring_string)
        i = spring_string_parts.index('?')
        for c in 'oD':
            spring_string_parts[i] = c
            get_all_spring_strings(''.join(spring_string_parts), strings)
    else:
        strings.append(spring_string)
    return strings


def get_regex(number_set):
    regex_parts = []
    for n in number_set:
        regex_parts.append('D{%s}' % n)
    return 'o{1,}'.join(regex_parts)


def part2(data):
    pass


def part1(data):
    # Too low: 8177 - I refactored and still got this number. Sadly, my previous (better) solution worked, but I was
    #                 keeping values in a dict and clobbering my own results without realizing.
    string_counts = 0
    for spring_string, numeric_data in data:
        populated_spring_strings = get_all_spring_strings(spring_string, [])
        spring_regex = get_regex(numeric_data)
        string_count = 0
        for populated_spring_string in populated_spring_strings:
            sub_spring_string = sub(spring_regex, 'x', populated_spring_string, count=1)
            if 'x' in sub_spring_string and 'D' not in sub_spring_string:
                string_count += 1
        string_counts += string_count
    print(string_counts)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
