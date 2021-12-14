import functools
import statistics


def read_line() -> dict[int, int]:
    return_value: dict[int, int] = {}
    with open("input.txt", "r") as fp:
        for i in fp.readline().replace("\n", "").split(","):
            return_value[int(i)] = return_value.get(int(i), 0) + 1

    return return_value


def distance(x_position: int, points: dict[int, int]) -> int:
    return sum([v * abs(x_position - k) for k, v in points.items()])


def search(points: dict[int, int]) -> int:
    guess = int(statistics.median(points.keys()))
    steps = int((max(points.keys()) - min(points.keys())) / 8)
    current_dist = distance(guess, points)
    prev, nxt = distance(guess - steps, points), distance(guess + steps, points)

    while True:
        if prev >= current_dist <= nxt:
            if steps == 1:
                return current_dist

            steps = int(steps / 2)
            prev, nxt = distance(guess - steps, points), distance(guess + steps, points)
            continue

        if prev < current_dist:
            guess -= steps
            prev, current_dist, nxt = distance(guess - steps, points), prev, current_dist
            continue

        guess += steps
        prev, current_dist, nxt = current_dist, nxt, distance(guess + steps, points)


def main():
    points = read_line()
    print(search(points))


if __name__ == "__main__":
    main()
