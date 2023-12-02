import argparse
from functools import reduce
from collections import defaultdict


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        games = fin.read().splitlines()

    parsed_games = defaultdict(list)
    for game in games:
        if game: # handles newline at EOF
            game_parts = game.split(': ')
            game_count = int(game_parts[0].split()[-1])
            game_rounds = game_parts[-1].split('; ')
            for game_round in game_rounds:
                game_round_parts = game_round.split(', ')
                parsed_game_round = {}
                for game_round_part in game_round_parts:
                    game_round_color_parts = game_round_part.split()
                    parsed_game_round[game_round_color_parts[-1]] = int(game_round_color_parts[0])
                parsed_games[game_count].append(parsed_game_round)

    return parsed_games


def part2(data):
    COLORS = ['red', 'green', 'blue']
    powers = []
    for game_number, game_rounds in data.items():
        max_colors = dict([(color, 0) for color in COLORS])
        for game_round in game_rounds:
            for color, color_count in game_round.items():
                if max_colors[color] < color_count:
                    max_colors[color] = color_count
        powers.append(reduce(lambda a,b: a*b, max_colors.values(), 1))
    print(sum(powers))


def part1(data):
    THRESHOLDS = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    possible_games = []
    for game_number, game_rounds in data.items():
        possible = True
        for game_round in game_rounds:
            for color, count in game_round.items():
                if count > THRESHOLDS[color]:
                    possible = False
                    break
            if not possible:
                break
        if possible:
            possible_games.append(game_number)

    print(sum(possible_games))



def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
