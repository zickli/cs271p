import os


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
