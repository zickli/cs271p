import multiprocessing
import random
from common import LRUCache, unify_path, read_graph


class StochasticLocalSearch:
    def __init__(self, graph, maximum, cache_size):
        self.g = graph
        self.max = maximum
        self.n = len(graph)
        self.best_path = random.sample(range(self.n), self.n)
        self.best_cost = self.cost(self.best_path)
        self.number_of_iterations = 0
        self.current_path = self.best_path.copy()
        self.current_cost = self.best_cost
        self.cache = LRUCache(capacity=cache_size)

    def cost(self, path):
        return sum(self.g[path[i - 1]][path[i]] for i in range(len(path)))

    def update_cost(self, i):
        # 获取交换后的节点
        path = self.current_path
        graph = self.g
        p = (i + 1) % self.n
        node1, node2 = path[i], path[p]

        p2 = (i + 2) % self.n
        old_weight = graph[path[i - 1]][node1] + graph[node1][node2] + graph[node2][path[p2]]
        new_weight = graph[path[i - 1]][node2] + graph[node2][node1] + graph[node1][path[p2]]

        return self.current_cost - old_weight + new_weight

    def search(self):
        find = (0, 0)
        restart_time = 0
        max_cost = 0

        while self.number_of_iterations < self.max:
            self.number_of_iterations += 1
            # print(unify_path(self.current_path),self.current_cost)
            self.cache.put(tuple(unify_path(self.current_path)), self.current_cost)
            best_local_path = self.current_path.copy()
            best_local_cost = float('inf')

            for i in range(self.n):
                new_path = self.current_path.copy()
                p = (i + 1) % self.n
                new_path[i], new_path[p] = self.current_path[p], self.current_path[i]

                if tuple(unify_path(new_path)) in self.cache.cache:
                    continue
                else:
                    new_path_cost = self.update_cost(i)

                    if new_path_cost < best_local_cost:
                        best_local_path = new_path.copy()
                        best_local_cost = new_path_cost
                    if new_path_cost > max_cost:
                        max_cost = new_path_cost

            if best_local_cost < self.best_cost:
                self.best_path = best_local_path.copy()
                self.best_cost = best_local_cost
                find = (restart_time, self.number_of_iterations)
                self.current_path = best_local_path.copy()
                self.current_cost = best_local_cost
            elif random.random() * self.n > self.best_cost / best_local_cost:
                self.current_path = best_local_path.copy()
                self.current_cost = best_local_cost
            elif self.number_of_iterations < self.max:
                new_path = random.sample(range(self.n), self.n)  # random_permutation
                new_cost = self.cost(new_path)
                while self.cache.get(tuple(unify_path(new_path))) is not None or (new_cost > 2.5 * self.best_cost):
                    new_path = random.sample(range(self.n), self.n)
                    new_cost = self.cost(new_path)
                self.current_path = new_path
                restart_time = restart_time + 1
                # print("restart")
                self.current_cost = new_cost

        return self.best_path, self.best_cost

    @staticmethod
    def worker(graph):
        solution = StochasticLocalSearch(graph, 400000, 4096)
        return solution.search()

    @staticmethod
    def solve(graph, processes=4):
        graphs = (graph for _ in range(processes))
        with multiprocessing.Pool(processes=processes) as pool:
            results = pool.map(StochasticLocalSearch.worker, graphs)

        results.sort(key=lambda x: x[1])
        return results[0][0], results[0][1]


if __name__ == '__main__':
    import os
    import time
    from bnb_dfs import BranchAndBoundDfs

    path = r"data/benchmark/14_100_50_0.out"
    file_name = os.path.basename(path)
    print(file_name)
    g = read_graph(path)
    start_time = time.perf_counter()
    b1, b2 = StochasticLocalSearch.solve(g, processes=12)
    end_time = time.perf_counter()

    print(b2)
    print(unify_path(b1))
    print("Elapse_time_of_SLS:{}".format(end_time - start_time))

    solution = BranchAndBoundDfs(g)
    start_time = time.perf_counter()
    c = solution.solve()
    end_time = time.perf_counter()

    d = unify_path(c[:-1])
    print(d)
    print(c.cost)
    print("Elapse_time_of_bnb:{}".format(end_time - start_time))
