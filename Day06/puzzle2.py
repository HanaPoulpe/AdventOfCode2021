class Aquarium:
    cool_down = 7
    initial = 9

    def __init__(self, fishes: list[int]):
        self.fishes = [0] * (Aquarium.initial + 1)
        for f in fishes:
            self.fishes[f] += 1

    def cycle(self):
        self.fishes[Aquarium.initial] += self.fishes[0]
        self.fishes[Aquarium.cool_down] += self.fishes[0]

        for i in range(Aquarium.initial):
            self.fishes[i] = self.fishes[i + 1]

        self.fishes[Aquarium.initial] = 0

    def __len__(self):
        return sum(self.fishes)


def read_file() -> list[int]:
    with open("input.txt", "r") as fp:
        return [int(d) for d in fp.readline().replace("\n", "").split(",")]


def main():
    aquarium = Aquarium(read_file())

    for _ in range(256):
        aquarium.cycle()

    print(len(aquarium))


if __name__ == "__main__":
    main()
