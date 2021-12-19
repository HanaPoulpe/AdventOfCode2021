import functools
import queue
import statistics
import typing

BRACKET_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def read_file() -> list[str]:
    with open("input.txt", 'r') as fp:
        return [line.replace("\n", "") for line in fp.readlines()]

T = typing.TypeVar('T')

def iter_queue(q: queue.LifoQueue[T]) -> typing.Generator[T, None, None]:
    while not q.empty():
        yield q.get()


@functools.lru_cache()
def check_line(line: str) -> int:
    CLOSE = {
        "(": ")",
        "{": "}",
        "[": "]",
        "<": ">",
    }

    bracket_queue: queue.LifoQueue[str] = queue.LifoQueue()

    for c in line:
        if c in "([{<":
            bracket_queue.put(c)
        elif c in ")]}>":
            b = bracket_queue.get()
            if CLOSE[b] != c:
                return 0

    if bracket_queue.empty():
        return 0

    return functools.reduce(lambda i, v: (i * 5) + BRACKET_SCORE[CLOSE[v]],
                            iter_queue(bracket_queue), 0)


def main():
    lines = read_file()
    points = [check_line(line) for line in lines if check_line(line) != 0]
    print(statistics.median(points))

if __name__ == "__main__":
    main()
