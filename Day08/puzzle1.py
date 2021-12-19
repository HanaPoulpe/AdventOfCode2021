import typing


def open_file() -> list[typing.Tuple[list[str], list[str]]]:
    return_value: list[typing.Tuple[list[str], list[str]]] = []
    with open("input.txt", 'r') as fp:
        for line in fp.readlines():
            line = line.replace("\n", "")
            patterns, output = line.split(" | ")
            return_value.append((patterns.split(" "), output.split(" ")))

    return return_value


def main():
    output = [o for _, o in open_file()]
    count = sum([sum([1 for digit in line if len(digit) in [2, 4, 3, 7]]) for line in output])
    print(count)


if __name__ == '__main__':
    main()
