import re
from itertools import chain, islice

from utils import get_input


def parse(text):
    lines = iter(text.split("\n"))
    seeds = list(map(int, re.findall(r"(\d+)", next(lines))))
    next(lines)
    mappings = []
    while line := next(lines, None):
        if "map:" in line:
            mapping = {}
            while line := next(lines, None):
                dst_start, src_start, length = map(int, line.split(" "))
                mapping[range(src_start, src_start + length)] = dst_start
            mappings.append(mapping)
    return seeds, mappings


def get_location(seed, mappings):
    for mapping in mappings:
        for r, dst in mapping.items():
            if seed in r:
                seed = dst + (seed - r.start)
                break
    return seed


def split_range(r, mapping):
    xs = iter(sorted(mapping, key=lambda x: x.start))
    x = next(xs)
    start = r.start
    while x and start < r.stop:
        if start < x.start:
            yield range(start, x.start)
            start = x.start

        stop = min(r.stop, x.stop)
        if stop > start:
            jump = mapping[x] - x.start
            yield range(start + jump, stop + jump)
            start = stop
        x = next(xs, None)

    if start < r.stop:
        yield range(start, r.stop)


def pairwise(x):
    it = iter(x)
    while pair := tuple(islice(it, 2)):
        yield pair


def part1(seeds, mappings):
    return min(get_location(seed, mappings) for seed in seeds)


def part2(seeds, mappings):
    rs = (range(a, a + b) for a, b in pairwise(seeds))
    for mapping in mappings:
        rs = list(chain.from_iterable(split_range(r, mapping) for r in rs))
    return min(r.start for r in rs)


if __name__ == '__main__':
    text = get_input(5)
    seeds, mappings = parse(text)
    print(part1(seeds, mappings))
    print(part2(seeds, mappings))
