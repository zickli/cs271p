import heapq
from common import LRUCache


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
        self.visited_node = 0
        self.mst_cache = LRUCache(capacity=4096)

    def minimum_spanning_tree(self, path: Path):
        start_node = path[0]
        path = tuple(sorted(path))
        cached = self.mst_cache.get(path)
        if cached is not None:
            return cached

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

        self.mst_cache.put(path, mst_cost)
        return mst_cost

    def estimate_cost(self, path: Path):
        return path.cost + self.minimum_spanning_tree(path)

    def search(self, path: Path, domain: set):
        self.visited_node += 1
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
            new_paths.append((self.estimate_cost(new_path),
                              new_path))

        new_paths.sort(key=lambda p: p[0])

        for (estimate_cost, new_path) in new_paths:
            if estimate_cost > self.best_path.cost:
                continue

            new_domain = domain.copy()
            new_domain.remove(new_path[-1])
            self.search(new_path, new_domain)

    def solve(self):
        self.search(Path([], graph=self.g),
                    {x for x in range(0, len(self.g))})
        return self.best_path
