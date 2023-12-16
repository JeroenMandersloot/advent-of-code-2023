from collections import defaultdict

from utils import get_input


def compute_hash(value):
    res = 0
    for c in map(ord, value):
        res += c
        res *= 17
        res %= 256
    return res


def part1(text):
    return sum(map(compute_hash, text.split(",")))


def part2(text):
    focal_lengths = {}
    boxes = defaultdict(list)
    for instruction in text.split(","):
        if "=" in instruction:
            label, focal_length = instruction.split("=")
            box = compute_hash(label)
            focal_lengths[label] = int(focal_length)
            if label not in boxes[box]:
                boxes[box].append(label)
        elif "-" in instruction:
            label = instruction[:-1]
            box = compute_hash(label)
            if label in boxes[box]:
                boxes[box].remove(label)

    res = 0
    for box, labels in boxes.items():
        for pos, label in enumerate(labels, start=1):
            res += (1 + box) * pos * focal_lengths[label]
    return res


if __name__ == '__main__':
    text = get_input(15, example=False)
    print(part1(text))
    print(part2(text))
