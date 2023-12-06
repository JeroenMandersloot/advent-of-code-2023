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
