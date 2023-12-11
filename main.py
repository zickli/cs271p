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
        p1 = os.path.join(os.path.dirname(__file__), '20_100.0_100.0.out')
        t1, sol = self.time_bnb_dfs(p1)
        print(t1)
        print(sol.best_path)

    def test_preset_bnb_dfs(self):
        p1 = os.path.join(os.path.dirname(__file__), 'data', 'preset', '5_0.0_10.0.out')
        t1, s1 = self.time_bnb_dfs(p1)

        p2 = os.path.join(os.path.dirname(__file__), 'data', 'preset', '10_0.0_1.0.out')
        t2, s2 = self.time_bnb_dfs(p2)

        print("5_0.0_10.0.out cost:", round(t1, 6), s1.best_path)
        print("10_0.0_1.0.out cost:", round(t2, 6), s2.best_path)

    @staticmethod
    def worker(filepath):
        filename = os.path.basename(filepath)
        meta = os.path.splitext(filename)[0]
        n, mean, var, i = map(float, meta.split('_'))
        print(os.getpid(), filename, n, mean, var, i)
        t, solution = TestTspSolving.time_bnb_dfs(filepath)
        result = (n, mean, var, i, t, solution.visited_node)
        return result

    @staticmethod
    def competition_worker(filepath):
        filename = os.path.basename(filepath)
        meta = os.path.splitext(filename)[0].split('-')
        n, k, u, v = map(int, (meta[2], meta[3], meta[4], meta[5]))
        print(os.getpid(), filename, n, k, u, v)
        t, solution = TestTspSolving.time_bnb_dfs(filepath)
        result = (n, k, u, v, t, solution.visited_node)
        return result

    def test_benchmark_bnb_dfs(self):
        filepaths = get_competition_benchmark()

        timeout = 10 * 60

        start_time = time.time()

        with (multiprocessing.Pool(processes=4) as pool):
            result_objects = [pool.apply_async(TestTspSolving.competition_worker, args=(fp,)) for fp in filepaths]

            results = []
            for r in result_objects:
                try:
                    results.append(r.get(timeout=timeout))
                except multiprocessing.context.TimeoutError:
                    print("A task timed out.")
                    break

        results.sort(key=lambda x: x[0])
        print(results)

        with open('benchmark_bnb_dfs_competition.txt', 'w') as f:
            for result in results:
                f.write(','.join(map(str, result)))
                f.write('\n')

        # Check if total running time exceeded 10 minutes
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print(f"Total runtime exceeded 10 minutes: {elapsed_time:.2f} seconds")


def test_draw_plot(self):
        import matplotlib.pyplot as plt
        import csv

        def draw_line(filepath):
            data = dict()
            with open(filepath) as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')

                for row in csvreader:
                    key = int(float(row[0]))
                    if key not in data:
                        data[key] = list()
                    data[key].append(float(row[4]))

            x = sorted(data.keys())
            y = [sum(data[k]) / len(data[k]) for k in x]
            plt.plot(x, y)
            print(x)
            print(y)

        draw_line('benchmark_bnb_dfs_cache.txt')
        draw_line('benchmark_bnb_dfs_nocache.txt')
        draw_line('benchmark_bnb_dfs_no_heuristic.txt')
        plt.show()


if __name__ == '__main__':
    unittest.main()
