from utils import get_input


def solve(xs):
    if not any(xs):
        return 0
    return xs[-1] + solve([b - a for a, b in zip(xs, xs[1:])])


if __name__ == '__main__':
    lines = get_input(9, example=False, lines=True)
    sequences = [list(map(int, line.split())) for line in lines]
    print(sum(map(solve, sequences)))
    print(sum(map(solve, map(list, map(reversed, sequences)))))
