from itertools import product

from utils import BaseGrid, get_input


class Grid(BaseGrid):
    def get_connections(self, x, y):
        for d in self.get_openings(x, y):
            if self.is_connected(x, y, d):
                yield self.get_neighbour(x, y, d)

    def is_connected(self, x, y, d):
        try:
            xn, yn = self.get_neighbour(x, y, d)
            opposite = self.D4[(self.D4.index(d) + 2) % 4]
            return opposite in self.get_openings(xn, yn)
        except IndexError:
            return False

    def get_openings(self, x, y):
        c = self.grid[y][x]
        if c in "SJL|┃┗┛": yield "N"  # North
        if c in "SFL-━┗┏": yield "E"  # East
        if c in "SF7|┃┓┏": yield "S"  # South
        if c in "SJ7-━┓┛": yield "W"  # West


def find_path(grid):
    s = grid.search("S")
    grid.set_position(s)
    path = [grid.pos]
    seen = set(path)
    prev = None
    while s not in (ps := set(grid.get_connections(*grid.pos))) or prev == s:
        p = next(p for p in ps if p not in seen)
        prev = grid.pos
        grid.set_position(*p)
        path.append(p)
        seen.add(p)
    return path


def part1(grid):
    path = find_path(grid)
    return len(path) // 2


def part2(grid):
    path = find_path(grid)
    rpath = {v: k for k, v in enumerate(path)}
    loop = set(path)
    seen = set(path)
    options = set(product(range(grid.width), range(grid.height))) - seen
    inside = set()
    outside = set()
    while options:
        is_inside = True
        queue = [next(iter(sorted(options)))]
        slips = set()
        area = set()
        while queue:
            c = queue.pop(0)
            if c in area or c in seen:
                continue
            if grid.is_border(*c):
                is_inside = False
            area.add(c)
            neighbours = set(grid.get_neighbours(*c, diagonal=True))
            queue += neighbours - seen - area
            slip_candidates = {
                                  frozenset({a, b})
                                  for a in neighbours.intersection(loop)
                                  for b in
                                  set(grid.get_neighbours(*a)).intersection(
                                      loop).intersection(neighbours)
                                  if path[rpath[a] - 1] != b and path[
                    rpath[b] - 1] != a
                              } - slips

            while slip_candidates:
                slip_queue = [next(iter(slip_candidates))]
                while slip_queue:
                    slip = slip_queue.pop(0)
                    if slip in slips:
                        continue
                    slips.add(slip)
                    a, b = slip
                    a_neighbours = set(grid.get_neighbours(*a, diagonal=True))
                    b_neighbours = set(grid.get_neighbours(*b, diagonal=True))
                    joint_neighbours = a_neighbours.intersection(b_neighbours)
                    if joint_neighbours.intersection(outside):
                        is_inside = False
                    queue += joint_neighbours - seen - area

                    slip_continuations = set()
                    for j in joint_neighbours.intersection(loop):
                        if path[rpath[j] - 1] != b and path[rpath[b] - 1] != j:
                            slip_continuations.add(frozenset({j, b}))
                        if path[rpath[j] - 1] != a and path[rpath[a] - 1] != j:
                            slip_continuations.add(frozenset({a, j}))

                    slip_queue += slip_continuations - slips
                slip_candidates -= slips

        if is_inside:
            inside |= area
        else:
            outside |= area
        seen |= area
        options -= seen
    return sorted(inside)


if __name__ == '__main__':
    grid = Grid(get_input(10, example=True, lines=True))
    path = set(find_path(grid))
    print(part1(grid))
    inside = part2(grid)
    for pos in inside:
        grid[pos] = "I"
    for pos in product(range(grid.width), range(grid.height)):
        if pos not in path and pos not in inside:
            grid[pos] = "O"
    table = str.maketrans("FJ7L-|", "┏┛┓┗━┃")
    print(len(inside))
