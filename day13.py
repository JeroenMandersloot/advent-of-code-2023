from utils import get_input


def find_mirrors(grid, num_smudges=0):
    translation = str.maketrans(".#", "01")
    lines = grid.translate(translation).split("\n")
    return (
        find_vertical_mirrors(lines, num_smudges),
        find_horizontal_mirrors(lines, num_smudges)
    )


def find_vertical_mirrors(lines, num_smudges=0):
    lines = list(map("".join, zip(*lines)))
    return find_horizontal_mirrors(lines, num_smudges)


def find_horizontal_mirrors(lines, num_smudges=0):
    numbers = [int(line, 2) for line in lines]
    height = len(numbers)
    for y in range(1, height):
        i = min(y, height - y)
        if num_smudges == sum(
                bin(a ^ b).count("1")
                for a, b in zip(
                    numbers[y:y + i],
                    reversed(numbers[y - i:y])
                )
        ):
            return y
    return 0


if __name__ == '__main__':
    text = get_input(13, example=False, lines=False)
    grids = text.split("\n\n")

    # Part 1
    vms, hms = zip(*map(find_mirrors, grids))
    print(sum(vms) + sum(hms) * 100)

    # Part 2
    vms, hms = zip(*(find_mirrors(grid, 1) for grid in grids))
    print(sum(vms) + sum(hms) * 100)
