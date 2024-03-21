# !/usr/bin/env python3


def reset_temp(filename: str) -> None:
    with open(filename, "w") as f:
        f.write("# !/usr/bin/env python3")


if __name__ == "__main__":
    reset_temp("temp.py")
