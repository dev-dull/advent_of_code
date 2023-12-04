import argparse
from copy import copy
from functools import reduce


class Scratchcards(dict):
    def add_cards(self, raw_scratchchards):
        for scratchcard in raw_scratchchards:
            card_parts = scratchcard.split(': ')
            card_number = int(card_parts[0].split()[-1])
            played_numbers_raw, winning_numbers_raw = card_parts[1].split(' | ')
            played_numbers = [int(n) for n in played_numbers_raw.split()]
            winning_numbers = [int(n) for n in winning_numbers_raw.split()]
            winning_picks = list(filter(lambda n: n in winning_numbers, played_numbers))
            self[card_number] = {
                'played_numbers': played_numbers,
                'winning_numbers': winning_numbers,
                'winning_picks': winning_picks,
                'card_score': int(reduce(lambda a,b: a*2, winning_picks, .5))
            }


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    scratchcards = Scratchcards()
    scratchcards.add_cards(lines)
    return scratchcards


def count_wins(scratchcards, wins):
    new_wins = []
    for win in wins:
        for wi, _ in enumerate(scratchcards[win]['winning_picks']):
            new_wins.append(win+wi+1)
    if new_wins:
        return len(wins)+count_wins(scratchcards, new_wins)
    return len(wins)+len(new_wins)

def part2(scratchcards):
    # low: 13114316
    wins = count_wins(scratchcards, scratchcards.keys())
    print(wins)

def part1(scratchcards):
    total_score = 0
    for card_number, data in scratchcards.items():
        total_score += data['card_score']
    print(total_score)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
