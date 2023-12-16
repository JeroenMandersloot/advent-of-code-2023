from itertools import chain

from utils import BaseGrid, get_input


def solve(grid, initial):
    beams = [initial]
    history = set()
    while beams:
        new_beams = []
        history |= set(beams)
        for (x, y, d) in beams:
            c = grid[(x, y)]
            if c == "|" and d in "EW":
                y1 = y - 1
                y2 = y + 1
                if (x, y1) in grid:
                    new_beams.append((x, y1, "N"))
                if (x, y2) in grid:
                    new_beams.append((x, y2, "S"))

            elif c == "-" and d in "NS":
                x1 = x - 1
                x2 = x + 1
                if (x1, y) in grid:
                    new_beams.append((x1, y, "W"))
                if (x2, y) in grid:
                    new_beams.append((x2, y, "E"))

            elif c == "/":
                x, y, d = {
                    "N": (x + 1, y, "E"),
                    "E": (x, y - 1, "N"),
                    "S": (x - 1, y, "W"),
                    "W": (x, y + 1, "S"),
                }[d]
                if (x, y) in grid:
                    new_beams.append((x, y, d))

            elif c == "\\":
                x, y, d = {
                    "N": (x - 1, y, "W"),
                    "E": (x, y + 1, "S"),
                    "S": (x + 1, y, "E"),
                    "W": (x, y - 1, "N"),
                }[d]
                if (x, y) in grid:
                    new_beams.append((x, y, d))

            else:
                try:
                    new_beams.append((*grid.get_neighbour(x, y, d), d))
                except IndexError:
                    pass
        beams = set(new_beams) - history

    return len({tuple(pos) for *pos, _ in history})


if __name__ == '__main__':
    grid = BaseGrid(get_input(16, example=False, lines=True))
    print(solve(grid, (0, 0, "E")))
    candidates = chain.from_iterable((
        ((x, 0, "S") for x in range(grid.width)),
        ((x, grid.height - 1, "N") for x in range(grid.width)),
        ((0, y, "E") for y in range(grid.height)),
        ((grid.width - 1, y, "W") for y in range(grid.height)),
    ))
    print(max(solve(grid, candidate) for candidate in candidates))
