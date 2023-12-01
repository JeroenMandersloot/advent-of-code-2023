import os


def get_input(day: int, example: bool = False) -> str:
    basename = "example" if example else "day"
    path = os.path.join("inputs", f"{basename}{day:02}.txt")
    with open(path, "r") as f:
        return f.read()
