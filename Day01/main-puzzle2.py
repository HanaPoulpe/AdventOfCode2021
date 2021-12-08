"""Advent Of Code 2021 - Day 1"""


def main():
    with open("input2.txt", "r") as fp:
        measurements = fp.readlines()

    measurements = [int(i[:-1]) for i in measurements]
    increase_count = 0
    for a, b, c, d in zip(
        measurements[3:], measurements[2:-1], measurements[1:-2], measurements[:-3]
    ):
        print(f"{a=}, {b=}, {c=}, {d=} - {(a + b + c) >= (b + c + d)}")
        increase_count += 1 if (a + b + c) > (b + c + d) else 0

    print(increase_count)


if __name__ == "__main__":
    main()
