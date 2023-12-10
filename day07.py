from collections import Counter

from utils import get_input


def compute_score(hand):
    return {
        (1, 1, 1, 1, 1): 0,  # High
        (1, 1, 1, 2): 1,  # Pair
        (1, 2, 2): 2,  # Two pair
        (1, 1, 3): 3,  # Three of a kind
        (2, 3): 4,  # Full house
        (1, 4): 5,  # Four of a kind
        (5,): 6,  # Five of a kind
    }[tuple(sorted(Counter(hand).values()))]


class Hand:
    def __init__(self, hand, jokers=False):
        self.hand = hand
        self.jokers = jokers

    def __lt__(self, other):
        if self.score < other.score:
            return True
        if self.score > other.score:
            return False
        trans = "ZYX1V" if self.jokers else "ZYXWV"
        table = str.maketrans("AKQJT", trans)
        return self.hand.translate(table) < other.hand.translate(table)

    def __hash__(self):
        return hash(self.hand)

    @property
    def score(self):
        if self.jokers:
            chars = "23456789TQKA"
            return max(compute_score(self.hand.replace("J", c)) for c in chars)
        return compute_score(self.hand)


def compute_winnings(hands, bids):
    return sum(
        rank * bid
        for rank, (_, bid)
        in enumerate(sorted(dict(zip(hands, bids)).items()), start=1)
    )


if __name__ == '__main__':
    text = get_input(7, example=False, lines=True)
    hands, bids = zip(*map(str.split, text))
    bids = list(map(int, bids))
    print(compute_winnings(map(Hand, hands), bids))  # Part 1
    hands = [Hand(hand, jokers=True) for hand in hands]
    print(compute_winnings(hands, bids))  # Part 2
