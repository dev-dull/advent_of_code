import argparse
from functools import reduce


class RaceRecords(dict):
    def __getitem__(self, total_time):
        record_distance = super().__getitem__(total_time)
        distances = {}
        for button_time in range(1, total_time):
            distance = button_time * (total_time - button_time)
            if distance > record_distance:
                distances[button_time] = distance
        return distances


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()
    times = [int(t) for t in lines[0].split()[1:]]
    distances = [int(t) for t in lines[1].split()[1:]]

    return RaceRecords(zip(times, distances))


def part2(data):
    rekern = lambda values: int(''.join([str(t) for t in values]))
    time = rekern(data.keys())
    record = rekern(data.values())
    data = RaceRecords([(time, record)])
    part1(data)


def part1(data):
    faster_times_counts = []
    for time in data.keys():
        faster_times_counts.append(len(data[time]))
    print(reduce(lambda a,b: a*b, faster_times_counts, 1))

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
