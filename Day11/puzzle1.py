import dataclasses
import functools
import queue
import typing


@dataclasses.dataclass
class Octo:
    octo_map: list[list[int]] = dataclasses.field(default=list)
    max_x: int = dataclasses.field(init=False)
    max_y: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.max_x = len(self.octo_map[0])
        self.max_y = len(self.octo_map)

    def get(self, x: int, y: int) -> int:
        if not (0 <= x < self.max_x):
            return 0
        if not (0 <= y < self.max_y):
            return 0
        return self.octo_map[y][x]

    def update(self, x: int, y: int, updater: typing.Callable[[int], int]):
        if not (0 <= x < self.max_x):
            return
        if not (0 <= y < self.max_y):
            return

        self.octo_map[y][x] = updater(self.octo_map[y][x])

    def __iter__(self) -> typing.Generator[typing.Tuple[int, int], None, None]:
        for y, line in enumerate(self.octo_map):
            for x, _ in enumerate(line):
                yield x, y

    def increase(self):
        to_update: queue.SimpleQueue[typing.Tuple[int, int]] = queue.SimpleQueue()
        def updater(x: int, y: int, v: int) -> int:
            if v == 9:
                to_update.put((x - 1, y - 1))
                to_update.put((x, y - 1))
                to_update.put((x + 1, y - 1))
                to_update.put((x - 1, y))
                to_update.put((x + 1, y))
                to_update.put((x - 1, y + 1))
                to_update.put((x, y + 1))
                to_update.put((x + 1, y + 1))

            return v + 1

        [to_update.put((i, j)) for i, j in self]

        while not to_update.empty():
            i, j = to_update.get()
            self.update(i, j, lambda k: updater(i, j, k))

    def count_flashes(self) -> int:
        return functools.reduce(lambda i, v: i + int(self.get(v[0], v[1]) > 9), self, 0)

    def reset(self):
        for x, y in self:
            self.update(x, y, lambda v: v if v < 10 else 0)

    def next_step(self) -> int:
        self.increase()
        r = self.count_flashes()
        self.reset()
        return r


def read_file() -> list[list[int]]:
    with open("input.txt", "r") as fp:
        return [[int(v) for v in line.replace("\n", "")] for line in fp.readlines()]


def main():
    octo = Octo(read_file())
    flashes = functools.reduce(lambda i, v: i + v.next_step(), [octo for _ in range(100)], 0)
    print(flashes)


if __name__ == "__main__":
    main()
