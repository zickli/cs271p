import heapq


class Path(list):
    def __init__(self, *args, cost=0.0, graph=None, **kwargs):
        super().__init__(*args, **kwargs)
        if graph is None:
            graph = [[]]
        self.g = graph
        self.cost = cost

    def append(self, v):
        if len(self) > 0:
            self.cost += self.g[self[-1]][v]
        super().append(v)

    def copy(self) -> 'Path':
        return Path(self, cost=self.cost, graph=self.g)


class BranchAndBoundDfs:
    def __init__(self, graph):
        self.g = graph
        self.n = len(graph)
        self.best_path = Path([], cost=float('inf'))
        self.stat = 0

    def minimum_spanning_tree(self, path: Path):
        start_node = path[0]
        visited = set(path)
        edges = []
        for to, weight in enumerate(self.g[start_node]):
            if to != start_node:
                edges.append((weight, start_node, to))
        heapq.heapify(edges)

        mst_cost = 0.0

        while edges:
            weight, frm, to = heapq.heappop(edges)
            if to not in visited:
                visited.add(to)
                mst_cost += weight

                for next_to, next_weight in enumerate(self.g[to]):
                    if to == next_to:
                        continue
                    if next_to not in visited:
                        heapq.heappush(edges, (next_weight, to, next_to))

        return mst_cost

    def estimate_cost(self, path: Path):
        return path.cost + self.minimum_spanning_tree(path)

    def solve(self, path: Path, domain: set):
        self.stat += 1
        if len(path) == self.n:
            path.append(path[0])
            path.cost += self.g[path[-1]][path[0]]
            if path.cost < self.best_path.cost:
                self.best_path = path
            return

        new_paths = []
        for next_city in domain:
            new_path = path.copy()
            new_path.append(next_city)

            new_domain = domain.copy()
            new_domain.remove(next_city)

            new_paths.append((self.estimate_cost(new_path),
                              new_path,
                              new_domain))

        new_paths.sort(key=lambda p: p[0])

        for (estimate_cost, new_path, new_domain) in new_paths:
            if estimate_cost > self.best_path.cost:
                continue
            self.solve(new_path, new_domain)


def read_graph(file_path):
    graph = []
    with open(file_path, 'r') as file:
        size = int(file.readline().strip())
        for _ in range(size):
            row = list(map(float, file.readline().split()))
            graph.append(row)
    return graph


if __name__ == '__main__':
    g = read_graph("10_0.0_1.0.out")
    solution = BranchAndBoundDfs(g)
    solution.solve(Path([], graph=g), {x for x in range(0, len(g))})
    print(solution.best_path, solution.stat)
