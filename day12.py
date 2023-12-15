import re
from functools import lru_cache
from typing import Sequence

from utils import get_input


def parse(line, unfold=False):
    conditions, groups = line.split(" ")
    groups = list(map(int, groups.split(",")))
    if unfold:
        conditions = "?".join([conditions] * 5)
        groups *= 5
    return conditions, tuple(groups)


@lru_cache(maxsize=None)
def solve(line: str, groups: Sequence[int]):
    if not groups:
        if "#" not in line:
            return 1
        return 0

    groups = list(groups)

    if not line:
        return 0

    group = groups.pop(0)
    pattern = r"(?=([?#]{" + str(group) + "}([?.]|$)))"
    matches = re.finditer(pattern, line)

    res = 0
    for match in matches:
        idx = match.start() + len(match.group(1))
        if "#" in line[:match.start()]:
            break

        newline = re.sub(r"^\.+", "", line[idx:])
        res += solve(newline, tuple(groups))
    return res


if __name__ == '__main__':
    lines = get_input(12, example=False, lines=True)

    # Part 1
    conditions, groups = zip(*map(parse, lines))
    print(sum(solve(line, gs) for line, gs in zip(conditions, groups)))

    # Part 2
    conditions, groups = zip(*(parse(line, unfold=True) for line in lines))
    print(sum(solve(line, gs) for line, gs in zip(conditions, groups)))
