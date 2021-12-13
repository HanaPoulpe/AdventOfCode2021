def read_file() -> list[int]:
    with open("input.txt", "r") as fp:
        return [int(d) for d in fp.readline().replace("\n", "").split(",")]


def cycle(anglers: list[int]) -> list[int]:
    cool_down = 6
    inital = cool_down + 2

    class New:
        def __init__(self):
            self.v = 0

    n = New()

    def make_new(n: New):
        n.v += 1
        return cool_down

    return [a - 1 if a > 0 else make_new(n) for a in anglers] + ([inital] * n.v)


def main():
    anglers = read_file()

    for _ in range(80):
        print(anglers)
        anglers = cycle(anglers)

    print(len(anglers))


if __name__ == "__main__":
    main()
