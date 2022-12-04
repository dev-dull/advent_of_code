import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    while '' in lines:
        # pesky newline at EOF
        lines.remove('')

    return lines


def part2(input):
    teams = CleanTeams()
    for team in input:
        teams.add_team(team)

    teams.sort_teams()

    ct = 0
    for raw, team in teams.items():
        # because my results are sorted, I can get away with just one compare
        if team[0][1] >= team[1][0]:
            ct += 1
            print(raw)

    print(ct)


def part1(input):
    teams = CleanTeams()
    for team in input:
        teams.add_team(team)

    teams.sort_teams()

    ct = 0
    for raw, team in teams.items():
        # because my results are sorted, I can get away with just one compare
        if team[0][1] >= team[1][1]:
            ct += 1
            print(raw)

    print(ct)

class CleanTeams(dict):
    def __init__(self):
        super().__init__()

    def add_team(self, key):
        individuals = key.split(',')
        self[key] = [[int(i) for i in p.split('-')] for p in key.split(',')]

    def sort_teams(self):
        for k, team in self.items():
            # sort teams by starting zone for fewer comparisons later, for part 1
            # Sort on both start and end zones to handle case when start or end zones are the same zone in both pairs.
            # (e.g. [[2,4], [2,6]]] might stay in this wrong order if we only sort by index 0)
            team.sort(key=lambda team_member: team_member[1], reverse=True)
            team.sort(key=lambda team_member: team_member[0])

def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    input = get_input(args.test)
    # part1(input)
    part2(input)


if __name__ == '__main__':
    main()
