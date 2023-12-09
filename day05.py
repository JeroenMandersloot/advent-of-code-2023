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
    mappings.append(mapping)
    return seeds, mappings


def get_location(seed, mappings):
    for mapping in mappings:
        for r, dst in mapping.items():
            if seed in r:
                seed = dst + (seed - r.start)
                break
    return seed


def kjk(r, mapping):
    xs = iter(sorted(mapping, key=lambda x: x.start))
    x = next(xs)
    start = r.start
    while start < r.stop:
        if x and start < x.start:
            yield range(start, x.start)
            start = x.start

        if x:
            stop = min(r.stop, x.stop)
            jump = mapping[x] - x.start
        else:
            stop = r.stop
            jump = 0

        if stop > start:
            if start + jump == 0:
                print(start + jump, start, jump, x, mapping[x], r)
            yield range(start + jump, stop + jump)
            start = stop

        x = next(xs, None)


def asahfjhasjfhd(rs, mappings):
    for mapping in mappings:
        print(rs)
        print(mapping)
        rs = sorted(
            chain.from_iterable(kjk(r, mapping) for r in rs),
            key=lambda x: x.start
        )
        print(rs)
        print("---")
    return list(rs)


def pairwise(x):
    it = iter(x)
    while pair := tuple(islice(it, 2)):
        yield pair


def part1(seeds, mappings):
    return min(get_location(seed, mappings) for seed in seeds)


def part2(seeds, mappings):
    seeds = [range(a, a + b) for a, b in pairwise(seeds)]
    return min(r.start for r in asahfjhasjfhd(seeds, mappings))


if __name__ == '__main__':
    text = get_input(5, example=False)
    seeds, mappings = parse(text)
    print(part1(seeds, mappings))
    print(part2(seeds, mappings))
