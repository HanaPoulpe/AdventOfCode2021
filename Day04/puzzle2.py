import dataclasses
import typing


@dataclasses.dataclass
class BingoCard:
    board: list[list[typing.Tuple[int, bool]]]

    def __post_init__(self):
        if len(self.board) != 5:
            raise ValueError("BingoCard should be a 5x5 array")
        for line in self.board:
            if len(line) != 5:
                raise ValueError("BingoCard should be a 5x5 array")

    def check(self, number: int) -> bool:
        """Check the number in the card, return is the card won"""
        return_value = False
        for i, line in enumerate(self.board):
            for j, case in enumerate(line):
                if case[0] == number:
                    self.board[i][j] = (number, True)

        return self.is_winner()

    def is_winner(self) -> bool:
        for line in self.board:
            if sum([int(c) for _, c in line]) == len(line):
                return True

        for col in range(len(self.board[0])):
            if sum([int(x[col][1]) for x in self.board]) == len(self.board):
                return True

        return False

    def score(self) -> int:
        return sum([sum([v * int(not f) for v, f in x]) for x in self.board])


def read_input() -> typing.Tuple[list[int], list[BingoCard]]:
    with open("input1.txt", "r") as fp:
        draws = [int(x) for x in fp.readline()[:-1].split(",")]
        boards: list[BingoCard] = []

        buffer: list[list[typing.Tuple[int, bool]]] = []
        for line in fp.readlines():
            line = line.replace("\n", "")

            if buffer and not line:
                boards.append(BingoCard(buffer))
                buffer = []
            elif line:
                buffer.append([(int(i), False) for i in line.split(" ") if i.isnumeric()])

        if buffer:
            boards.append(BingoCard(buffer))

    return draws, boards


def main():
    draws, boards = read_input()

    last_win = 0

    for d in draws:
        scores = [w.score() for w in filter(lambda x: x.check(d), boards)]

        if scores:
            last_win = min(scores) * d
            boards = list(filter(lambda x: not x.is_winner(), boards))
            if not boards:
                break

    print(last_win)


if __name__ == "__main__":
    main()
