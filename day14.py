import re

from utils import get_input


def shift(column):
    def callback(match):
        return "".join(sorted(match.group(0), reverse=True))

    return re.sub(r"(?:^|(?<=#))[.O]+", callback, column)


def solve(state):
    return sum(len(c) - i for c in state for i, p in enumerate(c) if p == "O")


def part1(lines):
    return solve(map(shift, map("".join, zip(*lines))))


def part2(lines):
    current = map("".join, zip(*lines))

    def cycle(state):
        state = map(shift, state)  # North
        state = map("".join, zip(*state))
        state = map(shift, state)  # West
        state = map("".join, map(reversed, zip(*state)))
        state = map(shift, state)  # South
        state = map("".join, map(reversed, zip(*state)))
        state = map(shift, state)  # East
        return tuple(reversed(list(map("".join, map(reversed, zip(*state))))))

    history = dict()
    while current not in history:
        history[current] = len(history)
        current = cycle(current)

    interval = len(history) - history[current]
    remaining = (1000000000 - history[current]) % interval
    for _ in range(remaining):
        current = cycle(current)

    return solve(current)


if __name__ == '__main__':
    lines = get_input(14, example=False, lines=True)
    print(part1(lines))
    print(part2(lines))
