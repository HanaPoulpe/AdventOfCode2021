"""Advent of Code 2021 - Day3.2"""
import typing
from functools import reduce


def read_line() -> list[list[int]]:
    with open("input1.txt", 'r') as fp:
        return [[int(i) for i in line[:-1]] for line in fp.readlines()]


def report_filter(matrix: list[list[int]], col: int,
                  flt: typing.Callable[[int, int], int]) -> list[list[int]]:
    """Filter elements"""
    frequency: list[int] = reduce(lambda a, b: [i + j for i, j in zip(a, b)], matrix)
    keep = flt(frequency[col], len(matrix))
    return [x for x in filter(lambda x: keep == x[col], matrix)]


def main():
    lines = read_line()
    o2 = lines
    co2 = lines
    for i in range(len(lines)):
        if len(o2) > 1:
            o2 = report_filter(o2, i,
                               lambda x, l: int(x * 2 >= l)
                               if (x * 2) == l else (1 if (x * 2) > l else 0))
        if len(co2) > 1:
            co2 = report_filter(co2, i,
                                lambda x, l: int(x / l)
                                if x in [0, l] else (int(not int(x * 2 >= l))
                                                     if (x * 2) == l
                                                     else (1 if (x * 2) < l else 0)))

        if len(o2) == 1 and len(co2) == 1:
            break

    cvt = lambda x: int("".join(["1" if v == 1 else "0" for v in x[0]]), 2)
    o2 = cvt(o2)
    co2 = cvt(co2)

    print(f"{o2=}, {co2=}, {o2 * co2=}")


if __name__ == "__main__":
    main()
