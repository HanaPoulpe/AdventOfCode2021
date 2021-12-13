import dataclasses
import re
import typing


@dataclasses.dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def __post_init__(self):
        if self.x1 > self.x2:
            self.x1, self.x2 = self.x2, self.x1
        if self.y1 > self.y2:
            self.y1, self.y2 = self.y2, self.y1

    @classmethod
    def from_str(cls, string: str) -> 'Line':
        p1, p2 = string.split(" -> ")
        x1, y1 = p1.split(",")
        x2, y2 = p2.split(",")
        return Line(int(x1), int(y1), int(x2), int(y2))

    def each(self) -> typing.Generator[typing.Tuple[int, int], None, None]:
        for x in range(self.x1 - 1, self.x2):
            for y in range(self.y1 - 1, self.y2):
                yield x, y

class Map:
    def __init__(self, x: int, y: int):
        self.map = [[0 for _ in range(x + 1)] for _ in range(y + 1)]
        self.x_max = x
        self.y_max = y

    def update(self, line: Line) -> None:
        if line.y1 == line.y2:
            for x in range(line.x1 - 1, line.x2):
                self.map[x][line.y1] += 1
        elif line.x1 == line.x2:
            for y in range(line.y1 - 1, line.y2):
                self.map[line.x1][y] += 1
        else:
            return

    def count(self, flt: typing.Callable[[int], bool]) -> int:
        return sum([sum([1 for p in line if flt(p)]) for line in self.map])  # noqa

    def __str__(self):
        return "\n".join(["".join([str(cell) if cell != 0 else "." for cell in line]) for line in self.map])


def read_file() -> Map:
    lines: list[Line] = []
    max_x = 0
    max_y = 0
    with open("input1.txt", "r") as fp:
        for i_line in fp.readlines():
            o_line = Line.from_str(i_line.replace("\n", ""))
            lines.append(o_line)
            max_x = max([max_x, o_line.x1, o_line.x2])
            max_y = max([max_y, o_line.y1, o_line.y2])

    o_map = Map(max_x, max_y)
    [o_map.update(line) for line in lines]

    return o_map


def main():
    o_map = read_file()
    print(str(o_map))
    print(o_map.count(lambda x: x >= 2))


if __name__ == "__main__":
    main()
