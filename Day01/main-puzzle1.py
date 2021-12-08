"""Advent Of Code 2021 - Day 1"""


def main():
    with open("input.txt", "r") as fp:
        measurements = fp.readlines()

    measurements = [int(i[:-1]) for i in measurements]
    increase_count = 0
    for m, prev in zip(measurements[1:], measurements[:-1]):
        print(f"{m=}, {prev=} - {m >= prev}")
        increase_count += 1 if m >= prev else 0

    print(increase_count)


if __name__ == "__main__":
    main()
