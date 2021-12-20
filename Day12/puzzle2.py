from __future__ import annotations

import queue


class Path:
    def __init__(self):
        self.path: list[str] = list()
        self.has_twice = False

    def add(self, node: str) -> Path:
        has_twice = self.has_twice
        if node in ["start"] and self.path:
            return NoPath()
        if node.islower() and node in self.path:
            if self.has_twice:
                return NoPath()
            has_twice = True

        r = Path()
        r.path = self.path.copy()
        r.path.append(node)
        r.has_twice = has_twice
        return r

    def is_closed(self) -> bool:
        return self.path[-1] == "end"

    def current(self) -> str:
        return self.path[-1]

    def weight(self) -> int:
        r = 1
        for p, n in zip(self.path[1:-2], self.path[2:-1]):
            if p.isupper() and n.islower():
                r += 1
            elif p.islower() and n.isupper():
                r += 1

        return r

    def __bool__(self):
        return not not self.path

    def __len__(self):
        return len(self.path)

    def __hash__(self):
        return hash("-".join(self.path))


class NoPath(Path):
    def __bool__(self):
        return False

    def is_closed(self):
        return False

    def __hash__(self):
        return hash("")


class Graph:
    def __init__(self):
        self.nodes: dict[str, set[str]] = dict()

    def add_edge(self, a: str, b: str):
        if a not in self.nodes:
            self.nodes[a] = set()
        self.nodes[a].add(b)

        if b not in self.nodes:
            self.nodes[b] = set()
        self.nodes[b].add(a)

    def explore(self) -> int:
        paths: queue.SimpleQueue[Path] = queue.SimpleQueue()
        completed = 0
        paths.put(Path().add("start"))

        while not paths.empty():
            current_path = paths.get()

            for node in self.nodes[current_path.current()]:
                new_path = current_path.add(node)
                if new_path.is_closed():
                    completed += 1
                    continue

                if new_path:
                    paths.put(new_path)

        return completed


def read_file() -> Graph:
    graph = Graph()
    with open("input.txt", "r") as fp:
        [graph.add_edge(*line.replace("\n", "").split("-")) for line in fp.readlines()]
    return graph


def main():
    graph = read_file()
    paths = graph.explore()
    print(paths)


if __name__ == "__main__":
    main()
