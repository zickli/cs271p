import multiprocessing
import os
import unittest
import time
from bnb_dfs import BranchAndBoundDfs


class TestTspSolving(unittest.TestCase):
    @staticmethod
    def get_benchmark():
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'benchmark')
        # list all file from data_path
        filepaths = []
        for filename in os.listdir(data_path):
            filepaths.append(os.path.join(data_path, filename))

        return filepaths

    @staticmethod
    def get_small_benchmark():
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'small_benchmark')
        # list all file from data_path
        filepaths = []
        for filename in os.listdir(data_path):
            filepaths.append(os.path.join(data_path, filename))

        return filepaths

    @staticmethod
    def read_graph(filepath):
        graph = []
        with open(filepath, 'r') as file:
            size = int(file.readline().strip())
            for _ in range(size):
                row = list(map(float, file.readline().split()))
                graph.append(row)
        return graph

    @staticmethod
    def time_bnb_dfs(filepath):
        g = TestTspSolving.read_graph(filepath)
        solution = BranchAndBoundDfs(g)

        start_time = time.perf_counter()
        solution.solve()
        end_time = time.perf_counter()

        return end_time - start_time

    def test_bnb_dfs(self):
        p1 = os.path.join(os.path.dirname(__file__), 'data', 'benchmark', '13_100_20.out')
        t1 = self.time_bnb_dfs(p1)
        print(t1)

    def test_preset_bnb_dfs(self):
        p1 = os.path.join(os.path.dirname(__file__), 'data', 'preset', '5_0.0_10.0.out')
        t1 = self.time_bnb_dfs(p1)

        p2 = os.path.join(os.path.dirname(__file__), 'data', 'preset', '10_0.0_1.0.out')
        t2 = self.time_bnb_dfs(p2)

        print("5_0.0_10.0.out cost:", round(t1, 6))
        print("10_0.0_1.0.out cost:", round(t2, 6))

    @staticmethod
    def worker(filepath):
        filename = os.path.basename(filepath)
        meta = os.path.splitext(filename)[0]
        n, mean, var, i = map(float, meta.split('_'))
        print(filename, n, mean, var, i)
        result = (n, mean, var, i, TestTspSolving.time_bnb_dfs(filepath))
        return result

    def test_benchmark_bnb_dfs(self):
        filepaths = TestTspSolving.get_small_benchmark()

        with multiprocessing.Pool(processes=3) as pool:
            results = pool.map(TestTspSolving.worker, filepaths)

        results.sort(key=lambda x: x[0])
        print(results)
        with open('benchmark_bnb_dfs.txt', 'w') as f:
            for result in results:
                f.write(','.join(map(str, result)))
                f.write('\n')


if __name__ == '__main__':
    unittest.main()
