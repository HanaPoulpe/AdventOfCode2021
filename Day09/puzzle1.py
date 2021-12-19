import typing


def read_file() -> list[list[int]]:
    with open("input.txt", "r") as fp:
        return [[int(h) for h in line.replace("\n", "")] for line in fp.readlines()]


class HeightMap:
    MAX_X: int
    MAX_Y: int


def is_low_point(x: int, y: int, heightmap: list[list[int]]) -> bool:
    match (x, y):
        case (0, 0):
            hlist = (heightmap[1][0], heightmap[0][1])
        case (0, HeightMap.MAX_Y):
            hlist = (heightmap[y][1], heightmap[y - 1][0])
        case (HeightMap.MAX_X, 0):
            hlist = (heightmap[1][x], heightmap[0][x - 1])
        case (HeightMap.MAX_X, HeightMap.MAX_Y):
            hlist = (heightmap[y - 1][x], heightmap[y][x - 1])
        case (0, _):
            hlist = (heightmap[y - 1][0], heightmap[y + 1][0], heightmap[y][1])
        case (HeightMap.MAX_X, _):
            hlist = (heightmap[y - 1][x], heightmap[y + 1][x], heightmap[y][x - 1])
        case (_, 0):
            hlist = (heightmap[0][x - 1], heightmap[0][x + 1], heightmap[1][x])
        case (_, HeightMap.MAX_Y):
            hlist = (heightmap[y][x - 1], heightmap[y][x + 1], heightmap[y - 1][x])
        case _:
            hlist = (heightmap[y - 1][x], heightmap[y + 1][x],
                     heightmap[y][x - 1], heightmap[y][x + 1])

    return not [v for v in hlist if v <= heightmap[y][x]]


def iter_heightmap(heightmap: list[list[int]]) \
        -> typing.Generator[typing.Tuple[int, int], None, None]:
    for y, line in enumerate(heightmap):
        for x, _ in enumerate(line):
            yield x, y


def main():
    heightmap = read_file()
    HeightMap.MAX_Y = len(heightmap) - 1
    HeightMap.MAX_X = len(heightmap[0]) - 1
    sum_low_point = sum([heightmap[y][x] + 1 for x, y in iter_heightmap(heightmap)
                         if is_low_point(x, y, heightmap)])
    print(sum_low_point)


if __name__ == '__main__':
    main()
