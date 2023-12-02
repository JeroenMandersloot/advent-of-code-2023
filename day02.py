import contextlib
import re

from utils import get_input


def is_possible(line, red, green, blue):
    colors = {"red": red, "green": green, "blue": blue}
    for color, limit in colors.items():
        with contextlib.suppress(ValueError):
            if max(map(int, re.findall(fr"\d+(?= {color})", line))) > limit:
                return None
    return int(re.search(r"^Game (\d+):", line).group(1))


def get_power(line):
    colors = ["red", "green", "blue"]
    res = 1
    for color in colors:
        res *= max(map(int, re.findall(fr"\d+(?= {color})", line)))
    return res


if __name__ == '__main__':
    lines = get_input(2).split("\n")
    print(sum(filter(None, (is_possible(line, 12, 13, 14) for line in lines))))
    print(sum(map(get_power, lines)))
