import functools


class Graph:
    N = 3

    def __init__(self):
        self.vertexes = {0}  # points
        self.edges = set()  # lines

    def add_vertex(self, number):
        self.vertexes.add(number)
        self._calculate_edges(number)

    def _calculate_edges(self, number):
        lower = max(number - Graph.N, 0)
        upper = number + Graph.N

        for index in range(lower, upper + 1):
            if index == number:
                continue

            if index in self.vertexes:
                if number > index:
                    self.edges.add((index, number))
                else:
                    self.edges.add((number, index))

    def longest_path(self):
        start = min(self.vertexes)
        return self._longest_path(start, [])

    def all_paths(self):
        start = min(self.vertexes)
        all = self._all_paths(start, [])
        return all

    def count_all_paths(self):
        start = min(self.vertexes)
        all = self._count_all_paths(start)
        return all

    def _longest_path(self, starting_point, path):
        options = sorted([(a, b) for (a, b) in self.edges if a == starting_point])
        if len(options) > 0:
            (a, b) = options[0]
            return self._longest_path(b, path + [a])
        return path + [starting_point]

    def _all_paths(self, starting_point, path):
        options = sorted([(a, b) for (a, b) in self.edges if a == starting_point])
        if len(options) > 0:
            the_paths = []
            for (a, b) in options:
                a_path = self._all_paths(b, path + [a])
                if isinstance(a_path[0], list):
                    for item in a_path:
                        the_paths.append(item)
                else:
                    the_paths.append(a_path)

            return the_paths

        return path + [starting_point]

    @functools.lru_cache
    def _count_all_paths(self, starting_point):
        options = [(a, b) for (a, b) in self.edges if a == starting_point]
        if len(options) > 0:
            more = 0
            for (a, b) in options:
                new_counter = self._count_all_paths(b)
                more += new_counter

            return more

        return 1

    @staticmethod
    def _flatten_the_lists(lists):
        paths = []
        while len(lists) > 0:
            lists = sorted(Graph._flatten(lists), key=len)
            paths.append(lists[-1])
            lists = lists[:-1]
        return paths

    @staticmethod
    def _flatten(lists):
        try:
            flattend = [x for y in lists for x in y]
            if isinstance(flattend[-1][-1], list):
                return Graph._flatten(flattend)
            return flattend
        except (TypeError, IndexError):
            return lists


class AdapterGraph(Graph):
    def solution_a(self):
        path = self.longest_path()
        path = self._enchance_path(path)

        partition = {x: 0 for x in range(1, Graph.N + 1)}

        for (a, b) in zip(path[:-1], path[1:]):
            partition[b - a] += 1

        return self._calcalate_score(partition)

    def solution_b(self):
        return self.count_all_paths()

    @staticmethod
    def _enchance_path(path):
        path.sort()
        maximum = max(path) + Graph.N
        path += [maximum]
        return path

    @staticmethod
    def _calcalate_score(partition):
        return partition[1] * partition[3]


if __name__ == "__main__":
    with open("data.txt") as f:
        data = [int(x) for x in f.read().splitlines()]

        g = AdapterGraph()
        for item in data:
            g.add_vertex(item)

        print(g.solution_a())
        print(g.solution_b())
