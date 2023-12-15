import re
from functools import lru_cache

from utils import get_input


def parse(line, unfold=False):
    conditions, groups = line.split(" ")
    groups = list(map(int, groups.split(",")))
    if unfold:
        conditions = "?".join([conditions] * 5)
        groups *= 5
    return conditions, tuple(groups)


@lru_cache(maxsize=None)
def solve(line, groups):
    if not groups:
        return "#" not in line

    if not line:
        return 0

    group, *groups = groups
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
