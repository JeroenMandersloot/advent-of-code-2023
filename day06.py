import re
from functools import reduce
from operator import mul

from utils import get_input


def count_strategies(t, d):
    return sum(s * (t - s) > d for s in range(t + 1))


if __name__ == '__main__':
    text = get_input(6, example=False)
    times, distances = map(list, (
        map(int, re.findall(r"\d+", line))
        for line in text.split("\n")
    ))
    print(reduce(mul, map(count_strategies, times, distances), 1))  # Part 1
    time, distance = map(int, re.findall(r"\d+", text.replace(" ", "")))
    print(count_strategies(time, distance))  # Part 2
