from utils import BaseGrid, get_input


def count_distances(grid, dilation):
    galaxies = list(grid.finditer("#"))
    expanded_rows = {i for i, row in enumerate(grid.rows) if set(row) == {"."}}
    expanded_cols = {i for i, col in enumerate(grid.cols) if set(col) == {"."}}
    for i in range(len(galaxies)):
        x, y = galaxies[i]
        for xo, yo in galaxies[i + 1:]:
            cols = set(range(min(x, xo), max(x, xo)))
            rows = set(range(min(y, yo), max(y, yo)))
            a = len(expanded_cols.intersection(cols))
            b = len(expanded_rows.intersection(rows))
            yield (a + b) * dilation + len(cols) - a + len(rows) - b


if __name__ == '__main__':
    lines = get_input(11, example=False, lines=True)
    grid = BaseGrid(lines)
    print(sum(count_distances(grid, dilation=2)))
    print(sum(count_distances(grid, dilation=1000000)))
