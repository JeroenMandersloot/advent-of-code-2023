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


def compute_length(instructions, nodes, s, t):
    for src in nodes:
        if src.endswith(s):
            for i, step in enumerate(cycle(instructions), start=1):
                if (src := nodes[src][int(step == "R")]).endswith(t):
                    yield i
                    break


def lcm(nums):
    # https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
    res = 1
    for i in nums:
        res = res * i // gcd(res, i)
    return res


if __name__ == '__main__':
    lines = get_input(8, example=False, lines=True)
    instructions, nodes = parse(lines)
    print(next(compute_length(instructions, nodes, "AAA", "ZZZ")))
    print(lcm(compute_length(instructions, nodes, "A", "Z")))
