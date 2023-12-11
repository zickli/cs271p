import os
from collections import OrderedDict


def get_benchmark():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'benchmark')
    # list all file from data_path
    filepaths = []
    for filename in os.listdir(data_path):
        if filename.endswith('.out'):
            filepaths.append(os.path.join(data_path, filename))

    return filepaths


def get_small_benchmark():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'small_benchmark')
    # list all file from data_path
    filepaths = []
    for filename in os.listdir(data_path):
        if filename.endswith('.out'):
            filepaths.append(os.path.join(data_path, filename))

    return filepaths


def get_competition_benchmark():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'Competion')
    # list all file from data_path
    filepaths = []
    for filename in os.listdir(data_path):
        if filename.startswith('tsp-problem') and filename.endswith('.txt'):
            a, b, c, d = map(int, filename.split('-')[2: -1])
            filepaths.append((a, b, c, d, os.path.join(data_path, filename)))

    filepaths.sort()
    sorted_paths = [t[-1] for t in filepaths]
    print(sorted_paths)
    return sorted_paths


def read_graph(filepath):
    graph = []
    with open(filepath, 'r') as file:
        size = int(file.readline().strip())
        for _ in range(size):
            row = list(map(float, file.readline().split()))
            graph.append(row)
    return graph


def unify_path(path: []):
    length = len(path)
    i = 0
    for i in range(length):
        if path[i] == 0:
            break

    unified = path[i:] + path[: i]
    return unified


class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value
