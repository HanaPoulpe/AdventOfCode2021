"""Advent of Code 2021 - Day3.1"""
from functools import reduce


def test_value() -> list[list[int]]:
    return [[int(i) for i in line] for line in """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split("\n")]


def read_line() -> list[list[int]]:
    with open("input1.txt", 'r') as fp:
        return [[int(i) for i in line[:-1]] for line in fp.readlines()]


def main():
    lines = read_line()
    report: list[int] = reduce(lambda a, b: [i + j for i, j in zip(a, b)], lines)
    gamma = int(("".join(["1" if (x * 2) >= len(read_line()) else "0" for x in report])), 2)
    epsilon = int(("".join(["1" if (x * 2) <= len(read_line()) else "0" for x in report])), 2)

    print(f"{gamma=}, {epsilon=}: {gamma * epsilon}")


if __name__ == "__main__":
    main()
