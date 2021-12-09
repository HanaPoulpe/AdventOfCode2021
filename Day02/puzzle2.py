"""Advent of Code 2021 - Day 2.1"""
import typing


def read_commands() -> typing.Generator[typing.Tuple[str, int], None, None]:
    """Read commands"""
    with open("input2.txt", "r") as fp:
        for line in fp.readlines():
            command, value = line.split(" ")
            value = int(value)
            print(f"{command=}({value=})")
            yield command, value


def main():
    x, y, aim = 0, 0, 0

    for command, value in read_commands():
        match (command, value):
            case "forward", dx:
                x += dx
                y += aim * dx
            case "down", daim:
                aim += daim
            case "up", daim:
                aim -= daim
        print(f"{x=},{y=},{aim=}")

    print(x * y)


if __name__ == "__main__":
    main()
