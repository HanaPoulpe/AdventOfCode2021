import dataclasses
import functools
import typing


def xor(a, b) -> bool:
    return (a or b) and not (a and b)


@dataclasses.dataclass
class Data:
    input: list[set[str]]
    output: list[set[str]]
    led_map: dict[str, str] = dataclasses.field(init=False)

    def __post_init__(self):
        self.led_map = {
            "a": "",  #  aaa
            "b": "",  # b   c
            "c": "",  # b   c
            "d": "",  #  ddd
            "e": "",  # e   f
            "f": "",  # e   f
            "g": "",  #  ggg
        }
        self.numbers: list[set[str]] = [set() for _ in range(10)]
        self.numbers[8] = {"a", "b", "c", "d", "e", "f", "g"}

    def decode(self):
        # Bucketize numbers by len
        len_buckets: dict[int, list[set[str]]] = {i: list() for i in range(2, 8)}
        for digit in self.input:
            if digit not in len_buckets[len(digit)]:
                len_buckets[len(digit)].append(digit)

        if len_buckets[2]:
            self.numbers[1] = len_buckets[2][0]
        if len_buckets[3]:
            self.numbers[7] = len_buckets[3][0]
        if len_buckets[4]:
            self.numbers[4] = len_buckets[4][0]

        # explore 6 points aka 0, 6, 9
        for digit in len_buckets[6]:
            # Complete easy
            self.find2()

            if self.numbers[1] and len(self.numbers[1].intersection(digit)) == 1:  # 6
                self.numbers[6] = digit
            elif self.numbers[7] and len(self.numbers[7].intersection(digit)) == 1:
                self.numbers[6] = digit

            elif self.numbers[4] and len(self.numbers[4].difference(digit)) == 1:  # 0
                self.numbers[0] = digit

            elif self.numbers[4] and not self.numbers[4].difference(digit):  # 9
                self.numbers[9] = digit

            self.find1()

        # explore 5 points aka 2, 3, 5
        for digit in len_buckets[5]:
            self.find2()

            if self.numbers[4] and len(digit.intersection(self.numbers[4])) == 2:  # 2
                self.numbers[2] = digit
            elif self.numbers[5] and len(digit.intersection(self.numbers[5])) == 3:
                self.numbers[2] = digit
            elif self.numbers[9] and len(digit.intersection(self.numbers[9])) == 4:
                self.numbers[2] = digit

            elif (self.numbers[1] or self.numbers[7]) and not \
                    self.numbers[1].union(self.numbers[7]).difference(digit):  # 3
                self.numbers[3] = digit
            elif self.numbers[1] and len(digit.intersection(self.numbers[1])) == 2:
                self.numbers[3] = digit
            elif self.numbers[2] and len(digit.intersection(self.numbers[2])) == 4:
                self.numbers[3] = digit
            elif self.numbers[5] and len(digit.intersection(self.numbers[5])) == 4:
                self.numbers[3] = digit
            elif self.numbers[7] and len(digit.intersection(self.numbers[7])) == 3:
                self.numbers[3] = digit

            elif self.numbers[6] and len(digit.intersection(self.numbers[6])) == 5:  # 5
                self.numbers[5] = digit

            self.find1()

    def find1(self):
        # a
        if self.numbers[1] and self.numbers[7]:
            self.led_map["a"] = self.numbers[7].difference(self.numbers[1]).pop()
        elif self.numbers[1] and self.led_map["a"] and not self.numbers[7]:
            self.numbers[7] = self.numbers[1].union({self.led_map["a"]})

        # b
        if self.numbers[3] and self.numbers[4]:
            self.led_map["b"] = self.numbers[4].difference(self.numbers[3]).pop()

        # c
        if self.numbers[6]:
            self.led_map["c"] = self.numbers[8].difference(self.numbers[6]).pop()

        if (self.numbers[1] or self.numbers[3] or self.numbers[4] or
            self.numbers[7] or self.numbers[9]) and self.numbers[5]:
            self.led_map["c"] = self.numbers[1].union(self.numbers[3]).union(self.numbers[4]).\
                union(self.numbers[7]).union(self.numbers[9]).difference(self.numbers[5]).pop()

        # d
        if self.numbers[0]:
            self.led_map["d"] = self.numbers[8].difference(self.numbers[0]).pop()

        # e
        if self.numbers[9]:
            self.led_map["e"] = self.numbers[8].difference(self.numbers[9]).pop()

        # f
        if (self.numbers[5] or self.numbers[6]) and self.numbers[1]:
            self.led_map["f"] = self.numbers[1].intersection(
                self.numbers[5].union(self.numbers[6])).pop()

        # g
        if self.numbers[7] and self.numbers[3] and self.numbers[4]:
            self.led_map["g"] = self.numbers[3].difference(self.numbers[7].union(self.numbers[4]))\
                .pop()

    def find2(self):
        if not self.numbers[0] and "" not in {
            self.led_map["a"], self.led_map["b"], self.led_map["c"], self.led_map["e"],
            self.led_map["f"], self.led_map["g"]
        }:
            self.numbers[0] = {self.led_map["a"], self.led_map["b"], self.led_map["c"],
                               self.led_map["e"], self.led_map["f"], self.led_map["g"]}
        if not self.numbers[1] and "" not in {self.led_map["c"], self.led_map["f"]}:
            self.numbers[1] = {self.led_map["c"], self.led_map["f"]}

        if not self.numbers[2] and "" not in {
            self.led_map["a"], self.led_map["b"], self.led_map["d"], self.led_map["f"],
            self.led_map["g"]
        }:
            self.numbers[2] = {self.led_map["a"], self.led_map["c"], self.led_map["d"],
                               self.led_map["e"], self.led_map["g"]}

        if not self.numbers[3] and "" not in {
            self.led_map["a"], self.led_map["c"], self.led_map["d"], self.led_map["f"],
            self.led_map["g"]
        }:
            self.numbers[3] = {self.led_map["a"], self.led_map["c"], self.led_map["d"],
                               self.led_map["f"], self.led_map["g"]}

        if not self.numbers[4] and "" not in {
            self.led_map["b"], self.led_map["c"], self.led_map["d"], self.led_map["f"]
        }:
            self.numbers[4] = {self.led_map["b"], self.led_map["c"], self.led_map["d"],
                               self.led_map["f"]}

        if not self.numbers[5] and "" not in {
            self.led_map["a"], self.led_map["b"], self.led_map["d"], self.led_map["f"],
            self.led_map["g"]
        }:
            self.numbers[5] = {self.led_map["a"], self.led_map["b"], self.led_map["d"],
                               self.led_map["f"], self.led_map["g"]}

        if not self.numbers[6] and "" not in {
            self.led_map["a"], self.led_map["b"], self.led_map["d"], self.led_map["e"],
            self.led_map["f"], self.led_map["g"]
        }:
            self.numbers[6] = {self.led_map["a"], self.led_map["b"], self.led_map["d"],
                               self.led_map["e"], self.led_map["f"], self.led_map["g"]}

        if not self.numbers[7] and "" not in {
            self.led_map["a"], self.led_map["c"], self.led_map["f"]
        }:
            self.numbers[7] = {self.led_map["a"], self.led_map["c"], self.led_map["f"]}

        if not self.numbers[9] and "" not in {
            self.led_map["a"], self.led_map["b"], self.led_map["c"], self.led_map["d"],
            self.led_map["f"], self.led_map["g"]
        }:
            self.numbers[9] = {self.led_map["a"], self.led_map["b"], self.led_map["c"],
                               self.led_map["d"], self.led_map["f"], self.led_map["g"]}

    def is_solved(self) -> int | None:
        self.find2()

        output = ""
        for digit in self.output:
            for d, s in enumerate(self.numbers):
                if s == digit:
                    output += str(d)
                    break
            else:
                return None

        return int(output)

    def solve(self) -> int:
        for _ in range(10):
            self.decode()
            s = self.is_solved()

            if s is not None:
                return s
            continue

        raise ValueError("Not Solved")


def open_file() -> list[Data]:
    return_value: list[Data] = []
    with open("input.txt", 'r') as fp:
        for line in fp.readlines():
            line = line.replace("\n", "")
            patterns, output = line.split(" | ")
            return_value.append(Data(
                [{c for c in d} for d in patterns.split(" ")],
                [{c for c in d} for d in output.split(" ")]
            ))

    return return_value


def main():
    data = open_file()
    s = functools.reduce(lambda x, y: y.solve() + x, data, 0)
    print(s)


if __name__ == '__main__':
    main()
