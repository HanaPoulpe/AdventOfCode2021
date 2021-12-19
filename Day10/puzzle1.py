import functools
import queue

BRACKET_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def read_file() -> list[str]:
    with open("input.txt", 'r') as fp:
        return [line.replace("\n", "") for line in fp.readlines()]


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
                return BRACKET_SCORE[c]

    return 0


def main():
    lines = read_file()
    points = functools.reduce(lambda a, b: a + check_line(b), lines, 0)
    print(points)

if __name__ == "__main__":
    main()
