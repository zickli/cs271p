import os
from collections import OrderedDict


def get_benchmark():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'benchmark')
    # list all file from data_path
    filepaths = []
    for filename in os.listdir(data_path):
        filepaths.append(os.path.join(data_path, filename))

    return filepaths


def get_small_benchmark():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'small_benchmark')
    # list all file from data_path
    filepaths = []
    for filename in os.listdir(data_path):
        filepaths.append(os.path.join(data_path, filename))

    return filepaths


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
