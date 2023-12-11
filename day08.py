import re
from itertools import cycle
from math import gcd

from utils import get_input


def parse(lines):
    lines = iter(lines)
    instructions = next(lines)
    next(lines)
    nodes = {}
    for line in lines:
        src, *inst = re.findall(r"[0-9A-Z]+", line)
        nodes[src] = inst

    return instructions, nodes


def part1(instructions, nodes):
    src = "AAA"
    path = []
    steps = "LR"
    instructions = cycle(instructions)
    while src != "ZZZ":
        step = next(instructions)
        src = nodes[src][steps.index(step)]
        path.append(step)
    return path


def part2(instructions, nodes):
    src = [node for node in nodes if node.endswith("A")]
    intervals = [0 for _ in src]
    steps = "LR"
    for i, step in enumerate(cycle(instructions)):
        src = [nodes[x][steps.index(step)] for x in src]
        for j, x in enumerate(src):
            if x.endswith("Z"):
                intervals[j] = i + 1

        if all(intervals):
            break

    return lcm(intervals)


def lcm(nums):
    # https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
    res = 1
    for i in nums:
        res = res * i // gcd(res, i)
    return res


if __name__ == '__main__':
    lines = get_input(8, example=False, lines=True)
    instructions, nodes = parse(lines)
    print(len(part1(instructions, nodes)))
    print(part2(instructions, nodes))
