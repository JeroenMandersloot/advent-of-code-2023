# TODO: make pretty
import contextlib
import re
from collections import defaultdict
from operator import itemgetter

from utils import get_input


def get_symbol(lines, x, y):
    for xdiff in (-1, 0, 1):
        for ydiff in (-1, 0, 1):
            with contextlib.suppress(IndexError):
                ypos = y + ydiff
                xpos = x + xdiff
                if ypos < 0 or xpos < 0:
                    continue
                char = lines[ypos][xpos]
                if not char.isdigit() and char != ".":
                    return xpos, ypos, char
    return False


def jaap(lines):
    fff = defaultdict(set)
    for y, line in enumerate(lines):
        numbers = re.finditer(r"\d+", line)
        for match in numbers:
            number = int(match.group(0))
            xstart = match.start(0)
            xend = match.end(0)
            for x in range(xstart, xend):
                if b := get_symbol(lines, x, y):
                    fff[(number, y, xstart, xend)].add(b)
                    break

    return fff


def invert_result(r):
    res = defaultdict(set)
    for k, v in r.items():
        for _k in v:
            res[_k].add(k)
    return res


def part1(lines):
    r = jaap(lines)
    return sum(map(itemgetter(0), r))


def part2(lines):
    r = jaap(lines)
    r = invert_result(r)
    total = 0
    for (*_, char), values in r.items():
        if char == "*" and len(values) == 2:
            values = list(values)
            total += values[0][0] * values[1][0]
    return total


if __name__ == '__main__':
    text = get_input(3)
    lines = text.split("\n")
    print(part1(lines))
    print(part2(lines))
