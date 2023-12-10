import multiprocessing
import os
import unittest
import time
from common import *
from bnb_dfs import BranchAndBoundDfs


class TestTspSolving(unittest.TestCase):

    @staticmethod
    def time_bnb_dfs(filepath):
        g = read_graph(filepath)
        solution = BranchAndBoundDfs(g)

        start_time = time.perf_counter()
        solution.solve()
        end_time = time.perf_counter()

        return end_time - start_time, solution

    def test_bnb_dfs(self):
        p1 = os.path.join(os.path.dirname(__file__), 'data', 'benchmark', '13_100_20.out')
        t1, _ = self.time_bnb_dfs(p1)
        print(t1)

    def test_preset_bnb_dfs(self):
        p1 = os.path.join(os.path.dirname(__file__), 'data', 'preset', '5_0.0_10.0.out')
        t1, _ = self.time_bnb_dfs(p1)

        p2 = os.path.join(os.path.dirname(__file__), 'data', 'preset', '10_0.0_1.0.out')
        t2, _ = self.time_bnb_dfs(p2)

        print("5_0.0_10.0.out cost:", round(t1, 6))
        print("10_0.0_1.0.out cost:", round(t2, 6))

    @staticmethod
    def worker(filepath):
        filename = os.path.basename(filepath)
        meta = os.path.splitext(filename)[0]
        n, mean, var, i = map(float, meta.split('_'))
        print(os.getpid(), filename, n, mean, var, i)
        t, solution = TestTspSolving.time_bnb_dfs(filepath)
        result = (n, mean, var, i, t, solution.visited_node)
        return result

    def test_benchmark_bnb_dfs(self):
        filepaths = get_small_benchmark()

        with multiprocessing.Pool(processes=3) as pool:
            results = pool.map(TestTspSolving.worker, filepaths)

        results.sort(key=lambda x: x[0])
        print(results)
        with open('benchmark_bnb_dfs_1_cache.txt', 'w') as f:
            for result in results:
                f.write(','.join(map(str, result)))
                f.write('\n')


if __name__ == '__main__':
    unittest.main()
