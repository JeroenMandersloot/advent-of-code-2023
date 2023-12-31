import contextlib
import os
from typing import Sequence, Union


def get_input(
        day: int,
        example: bool = False,
        lines: bool = False
) -> Union[str, Sequence[str]]:
    basename = "example" if example else "day"
    path = os.path.join("inputs", f"{basename}{day:02}.txt")
    with open(path, "r") as f:
        text = f.read()

    return text.strip("\n").split("\n") if lines else text


class BaseGrid:
    D4 = "NESW"
    D8 = ["N", "E", "S", "W", "NE", "SE", "SW", "NW"]

    def __init__(self, grid, start=None, marker=None):
        if isinstance(grid, str):
            grid = grid.split("\n")
        self.grid = grid
        self.marker = marker
        self.pos = start

    def move(self, d, skip_errors=False):
        if self.pos is None:
            raise ValueError("No position")
        x, y = self.pos
        try:
            self.pos = self.get_neighbour(x, y, d)
        except IndexError:
            if not skip_errors:
                raise

    def __getitem__(self, pos):
        x, y = pos
        return self.grid[y][x]

    def __setitem__(self, pos, value):
        x, y = pos
        line = list(self.grid[y])
        line[x] = value
        self.grid[y] = "".join(line)

    def search(self, c):
        for y, line in enumerate(self.grid):
            with contextlib.suppress(ValueError):
                return line.index(c), y
        raise ValueError(f"Character {c} not found")

    def finditer(self, c):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == c:
                    yield x, y

    def set_position(self, x, y=None):
        if y is None:
            x, y = x
        self.pos = (x, y)

    def row(self, y):
        return self.grid[y]

    def col(self, x):
        return "".join(self.grid[y][x] for y in range(self.height))

    @property
    def rows(self):
        yield from self.grid

    @property
    def cols(self):
        return map(self.col, range(self.width))

    @property
    def width(self):
        return max(map(len, self.grid))

    @property
    def height(self):
        return len(self.grid)

    @staticmethod
    def turn_left(d):
        return {
            "N": "W",
            "W": "S",
            "S": "E",
            "E": "N",
        }[d]

    @staticmethod
    def turn_right(d):
        return {
            "N": "E",
            "E": "S",
            "S": "W",
            "W": "N",
        }[d]

    def is_border(self, x, y):
        return x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1

    def get_neighbour(self, x, y, d):
        x, y = {
            "N": (x, y - 1),
            "E": (x + 1, y),
            "S": (x, y + 1),
            "W": (x - 1, y),
            "NE": (x + 1, y - 1),
            "SE": (x + 1, y + 1),
            "SW": (x - 1, y + 1),
            "NW": (x - 1, y - 1),
        }[d]
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            raise IndexError(f"({x}, {y})")
        return x, y

    def get_neighbours(self, x, y, diagonal=False):
        ds = ["N", "E", "S", "W"]
        if diagonal:
            ds += ["NE", "SE", "SW", "NW"]
        for d in ds:
            with contextlib.suppress(IndexError):
                yield self.get_neighbour(x, y, d)

    def show(self):
        print(f"{self}\n")

    def __contains__(self, item):
        x, y = item
        return 0 <= x < self.width and 0 <= y < self.height

    def __hash__(self):
        return hash(str(self))

    def __iter__(self):
        yield from self.rows

    def __str__(self):
        if self.pos and self.marker:
            g = list(map(list, self.grid))
            x, y = self.pos
            g[y][x] = self.marker
            return "\n".join("".join(line) for line in g)
        return "\n".join(self.grid)
