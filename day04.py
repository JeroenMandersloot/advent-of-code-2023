import re

from utils import get_input


def parse(line):
    card, numbers = line.split(":")
    card = int(re.search(r"\d+", card).group(0))
    pattern = re.compile(r"(\d+)")
    winning, actual = map(pattern.findall, numbers.split("|", maxsplit=2))
    num_winning = sum(map(winning.__contains__, actual))
    return card, num_winning


def part1(lines):
    return sum(2 ** (n - 1) for _, n in map(parse, lines) if n)


def part2(lines):
    collection = dict.fromkeys(range(1, len(lines) + 1), 1)
    for card, num_winning in map(parse, lines):
        for w in range(num_winning):
            collection[card + 1 + w] += collection[card]
    return sum(collection.values())


if __name__ == '__main__':
    lines = get_input(4, lines=True)
    print(part1(lines))
    print(part2(lines))
