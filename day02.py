import re

from utils import get_input

LIMITS = {"red": 12, "green": 13, "blue": 14}


def is_possible(line):
    for color, limit in LIMITS.items():
        if max(map(int, re.findall(fr"\d+(?= {color})", line))) > limit:
            return None
    return int(re.search(r"^Game (\d+):", line).group(1))


def get_power(line):
    res = 1
    for color in ("red", "green", "blue"):
        res *= max(map(int, re.findall(fr"\d+(?= {color})", line)))
    return res


if __name__ == '__main__':
    lines = get_input(2).split("\n")
    print(sum(filter(None, map(is_possible, lines))))  # Part 1
    print(sum(map(get_power, lines)))  # Part 2
