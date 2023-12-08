import argparse


# For part 1
class CamelCardHands(list):
    class C(object):
        # C is for constants (and that's good enough for me)
        CARD_VALUE_LOOKUP = {}
        for i, c in enumerate(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']):
            CARD_VALUE_LOOKUP[c] = (i + 2)

    def append(self, line):
        hand, wager = line.split()

        hand_value = 0.0
        for i, f in enumerate([self.five_of_a_kind, self.four_of_a_kind, self.full_house, self.three_of_a_kind, self.two_pair, self.one_pair, lambda _, __: True]):
            if f(self, hand):
                hand_value = (6.0 - i)
                break

        for i, c in enumerate(hand):
            face_value = self.C.CARD_VALUE_LOOKUP[c]
            decimal_value = face_value / (100 ** (i + 1))
            hand_value += decimal_value

        hand_data = {
            'hand': hand,
            'wager': int(wager),
            'hand_value': hand_value
        }
        super().append(hand_data)

    @staticmethod
    def _counting_cards(hand, count, count_counts):
        counts = []
        for c in set(hand):
            counts.append(hand.count(c))
        return counts.count(count) == count_counts

    @staticmethod
    def five_of_a_kind(self, hand):
        return hand[0]*5 == hand

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


# For part 2
class WildCamelCardHands(CamelCardHands):
    class C(object):
        # C is for constants (and that's good enough for me)
        CARD_VALUE_LOOKUP = {}
        for i, c in enumerate(['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']):
            CARD_VALUE_LOOKUP[c] = (i + 1)

    @staticmethod
    def _wildcard_replace(self, hand, unique_card_count, combined_card_count):
        test_hand = hand
        hand_set = list(set(hand))
        wild_j = 'J'
        if 'J' in hand and len(hand_set) == unique_card_count:
            hand_set.remove('J')
            for c in hand_set:
                if test_hand.count(c) + test_hand.count('J') == combined_card_count:
                    if self.C.CARD_VALUE_LOOKUP[c] > self.C.CARD_VALUE_LOOKUP[wild_j]:
                        wild_j = c
        return hand if wild_j == 'J' else test_hand.replace('J', wild_j)

    @staticmethod
    def five_of_a_kind(self, hand):
        test_hand = self._wildcard_replace(self, hand, 2, 5)
        return super().five_of_a_kind(self, test_hand)

    @staticmethod
    def four_of_a_kind(self, hand):
        # QYYYY
        # QJYYY
        # QJJYY
        # QJJJY
        # QJJJJ
        test_hand = self._wildcard_replace(self, hand, 3, 4)
        return super().four_of_a_kind(self, test_hand)

    @staticmethod
    def full_house(self, hand):
        # 11222
        # 11J22
        test_hand = self._wildcard_replace(self, hand, 3, 3)
        return super().full_house(self, test_hand)

    @staticmethod
    def three_of_a_kind(self, hand):
        # 12333
        # 12J33
        # 12JJ3
        # 12JJJ
        test_hand = self._wildcard_replace(self, hand, 4, 3)
        return super().three_of_a_kind(self, test_hand)

    @staticmethod
    def two_pair(self, hand):
        # 11223
        # 11J23
        # if we had two instances of 'J' then we'd want to make it 3 of a kind
        test_hand = self._wildcard_replace(self, hand, 4, 4)
        return super().two_pair(self, test_hand)

    @staticmethod
    def one_pair(self, hand):
        # 11345
        # 1J345
        test_hand = self._wildcard_replace(self, hand, 5, 2)
        return super().one_pair(self, test_hand)


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().strip().splitlines()

    return lines


def part2(data):
    # Too low: 250162214 -- this was a YOLO test to see if I need to override the card match methods
    # Too low: 250848049 -- also failed on test input, so this is expected
    # Too low: 251027022 -- after fixing four_of_a_kind
    #          250273505 -- unsubmitted test
    camel_card_hands = WildCamelCardHands()
    for d in data:
        # it'd be nicer if we could just cast it, but this'll do for now.
        camel_card_hands.append(d)

    wager_score = []
    camel_card_hands.sort(key=lambda h: h['hand_value'])
    for i, hand in enumerate(camel_card_hands):
        wager_score.append(hand['wager'] * (i + 1))

    result = sum(wager_score)
    print(result)


def part1(data):
    camel_card_hands = CamelCardHands()
    for d in data:
        # it'd be nicer if we could just cast it, but this'll do for now.
        camel_card_hands.append(d)

    # too high: 251185712 - I failed to create a full_house() function. Bob Saget would be very sad for me.
    wager_score = []
    camel_card_hands.sort(key=lambda h: h['hand_value'])
    for i, hand in enumerate(camel_card_hands):
        wager_score.append(hand['wager'] * (i+1))

    result = sum(wager_score)
    print(result)


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2023 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
