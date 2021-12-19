import dataclasses
import queue
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


def find_basin_size(ox: int, oy: int, heightmap: list[list[int]]) -> int:
    @dataclasses.dataclass(slots=True, eq=False)
    class ExplorePoint:
        x: int
        y: int
        z: int
        left: bool
        right: bool
        up: bool
        down: bool

        def __hash__(self):
            return hash(f"{self.x=},{self.y=}")

        def __eq__(self, other):
            return self.x == other.x and self.y == self.y

    explore_queue: queue.Queue[ExplorePoint] = queue.Queue()
    explore_queue.put(ExplorePoint(ox, oy, heightmap[oy][ox],
                                   ox != 0, ox != HeightMap.MAX_X,
                                   oy != 0, oy != HeightMap.MAX_Y))
    points: set[ExplorePoint] = set()

    while not explore_queue.empty():
        ep = explore_queue.get()
        if ep in points:
            continue

        points.add(ep)

        if ep.left and 9 > heightmap[ep.y][ep.x - 1] > ep.z:
            explore_queue.put(ExplorePoint(
                ep.x - 1, ep.y, heightmap[ep.y][ep.x - 1],
                ep.x - 1 != 0, False,
                ep.y != 0, ep.y != HeightMap.MAX_Y
            ))

        if ep.right and 9 > heightmap[ep.y][ep.x + 1] > ep.z:
            explore_queue.put(ExplorePoint(
                ep.x + 1, ep.y, heightmap[ep.y][ep.x + 1],
                False, ep.x + 1 != HeightMap.MAX_X,
                ep.y != 0, ep.y != HeightMap.MAX_Y
            ))

        if ep.up and 9 > heightmap[ep.y - 1][ep.x] > ep.z:
            explore_queue.put(ExplorePoint(
                ep.x, ep.y - 1, heightmap[ep.y - 1][ep.x],
                ep.x != 0, ep.x != HeightMap.MAX_X,
                ep.y - 1 != 0, False
            ))

        if ep.down and 9 > heightmap[ep.y + 1][ep.x] > ep.z:
            explore_queue.put(ExplorePoint(
                ep.x, ep.y + 1, heightmap[ep.y + 1][ep.x],
                ep.x != 0, ep.x != HeightMap.MAX_X,
                False, ep.y + 1 != HeightMap.MAX_Y
            ))

    return len(points)


def main():
    heightmap = read_file()
    HeightMap.MAX_Y = len(heightmap) - 1
    HeightMap.MAX_X = len(heightmap[0]) - 1
    low_points = [(x, y) for x, y in iter_heightmap(heightmap) if is_low_point(x, y, heightmap)]

    b0, b1, b2 = 0, 0, 0
    for x, y in low_points:
        b_size = find_basin_size(x, y, heightmap)
        if b_size > b0:
            b0, b1, b2 = b_size, b0, b1
        elif b_size > b1:
            b1, b2 = b_size, b1
        elif b_size > b2:
            b2 = b_size

    print(f"{b0=}, {b1=}, {b2=} = {b0 * b1 * b2}")


if __name__ == '__main__':
    main()
