from __future__ import annotations

import queue


class Path:
    def __init__(self):
        self.path: list[str] = list()

    def add(self, node: str) -> Path:
        if node.islower() and node in self.path:
            return NoPath()

        r = Path()
        r.path = self.path.copy()
        r.path.append(node)
        return r

    def is_closed(self) -> bool:
        return self.path[-1] == "end"

    def current(self) -> str:
        return self.path[-1]

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

    def explore(self) -> set[Path]:
        paths: queue.SimpleQueue[Path] = queue.SimpleQueue()
        completed: set[Path] = set()
        paths.put(Path().add("start"))

        while not paths.empty():
            current_path = paths.get()

            for node in self.nodes[current_path.current()]:
                new_path = current_path.add(node)
                if new_path.is_closed():
                    completed.add(new_path)
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
    print(len(paths))


if __name__ == "__main__":
    main()
