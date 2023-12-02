import re

from utils import get_input

NUMS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
REPLACEMENTS = {w: str(i) for i, w in enumerate(NUMS, start=1)}


def get_calibration_value(line, allow_replacements=False) -> int:
    digits = []
    pattern = re.compile(fr"^({'|'.join(REPLACEMENTS)})")
    for i, c in enumerate(line):
        if c.isdigit():
            digits.append(c)
        elif allow_replacements and (m := pattern.search(line[i:])):
            digits.append(REPLACEMENTS[m.group(0)])
    return int(digits[0] + digits[-1])


if __name__ == '__main__':
    lines = get_input(1).split("\n")
    print(sum(map(get_calibration_value, lines)))  # Part 1
    print(sum(get_calibration_value(line, True) for line in lines))  # Part 2
