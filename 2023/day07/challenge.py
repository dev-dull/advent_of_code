import argparse


class C(object):
    # C is for constants (and that's good enough for me)
    CARD_VALUE_LOOKUP = {}
    for i, c in enumerate(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']):
        CARD_VALUE_LOOKUP[c] = (i+2)


class CamelCardHands(list):
    def append(self, line):
        hand, wager = line.split()

        hand_value = 0.0
        for i, f in enumerate([self.five_of_a_kind, self.four_of_a_kind, self.full_house, self.three_of_a_kind, self.two_pair, self.one_pair, lambda _, __: True]):
            if f(self, hand):
                hand_value = (6.0 - i)
                break

        for i, c in enumerate(hand):
            face_value = C.CARD_VALUE_LOOKUP[c]
            decimal_value = face_value / (100 ** (i + 1))
            hand_value += decimal_value

        hand_data = {
            'hand': hand,
            'wager': int(wager),
            'hand_value': hand_value
        }
        super().append(hand_data)

    @staticmethod
    def five_of_a_kind(self, hand):
        return hand[0]*5 == hand

    @staticmethod
    def _counting_cards(hand, count, count_counts):
        counts = []
        for c in set(hand):
            counts.append(hand.count(c))
        return counts.count(count) == count_counts

    @staticmethod
    def four_of_a_kind(self, hand):
        return self._counting_cards(hand, 4, 1)

    @staticmethod
    def full_house(self, hand):
        return self._counting_cards(hand, 3, 1) and self._counting_cards(hand, 2, 1)

    @staticmethod
    def three_of_a_kind(self, hand):
        return self._counting_cards(hand, 3, 1)

    @staticmethod
    def two_pair(self, hand):
        return self._counting_cards(hand, 2, 2)

    @staticmethod
    def one_pair(self, hand):
        return self._counting_cards(hand, 2, 1)


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    camel_card_hands = CamelCardHands()
    for line in lines:
        # it'd be nicer if we could just cast it, but this'll do for now.
        camel_card_hands.append(line)

    return camel_card_hands


def part2(data):
    pass


def part1(data):
    # too high: 251185712 - I failed to create a full_house() function. Bob Saget would be very sad for me.
    wager_score = []
    y = data.sort(key=lambda h: h['hand_value'])
    for i, hand in enumerate(data):
        wager_score.append(hand['wager'] * (i+1))

    result = sum(wager_score)
    print(result)



def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
