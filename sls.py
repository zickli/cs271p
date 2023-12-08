import random
from bnb_dfs import *
from collections import OrderedDict






def update_cost(old_cost, graph, path, i):
    # 获取交换后的节点
    node1, node2 = path[i], path[i + 1]

    # 获取交换前和交换后的边的权重
    if i+2==len(path):
        old_weight = graph[path[i - 1]][node1] + graph[node1][node2] + graph[node2][path[0]]
        new_weight = graph[path[i - 1]][node2] + graph[node2][node1] + graph[node1][path[0]]
    else:

        old_weight = graph[path[i - 1]][node1] + graph[node1][node2] + graph[node2][path[i + 2]]
        new_weight = graph[path[i - 1]][node2] + graph[node2][node1] + graph[node1][path[i + 2]]



    # 更新旧的成本
    return old_cost - old_weight + new_weight


def Cost(graph, path):
    return sum(graph[path[i-1]][path[i]] for i in range(len(path)))

def add_path_to_cache(path, cost,cache, capacity):
    # 将路径添加到有序字典
    cache[tuple(path)] = cost

    # 检查字典长度是否超过容量
    if len(cache) > capacity:
        # 如果超过容量，从字典的开头删除最早插入的元素
        cache.popitem(last=False)

def stochastic_local_search(graph,maximum):
    N = len(graph)
    best_path = random.sample(range(N), N)  # random_permutation
    best_cost = Cost(g,best_path)
    current_path = best_path.copy()
    current_cost = best_cost
    number_of_iterations = 0
    cache = OrderedDict()
    cache_capacity = N*N
    update_flag = 1
    while update_flag:
        number_of_iterations += 1
        add_path_to_cache(current_path,current_cost,cache,cache_capacity)
        update_flag = 0
        best_local_path = current_path.copy()
        best_local_cost =  float('inf')
        for i in range(N - 1):
            new_path = current_path.copy()
            new_path[i], new_path[i + 1] = current_path[i + 1], current_path[i]

            if tuple(new_path) in cache:
                continue
            else:
                #new_path_cost = Cost(g,new_path)
                new_path_cost = update_cost(current_cost,g,current_path,i)
                if new_path_cost < best_local_cost:
                    best_local_path = new_path.copy()
                    best_local_cost = new_path_cost
        if best_local_cost < best_cost:
            best_path= best_local_path.copy()
            best_cost = best_local_cost
            current_path = best_local_path.copy()
            current_cost = best_local_cost

            update_flag = 1
        elif random.random() > best_cost / best_local_cost:
            current_path = best_local_path.copy()
            current_cost = best_local_cost
            update_flag=1
        elif number_of_iterations<maximum:
            new_path = random.sample(range(N), N)  # random_permutation
            while tuple(new_path) in cache.keys():
                new_path = random.sample(range(N), N)
            current_path = new_path
            current_cost = Cost(g,new_path)
            update_flag = 1


    return best_path,best_cost



if __name__ == '__main__':
    g = read_graph("10_0.0_1.0.out")
    for i in g:
        print(i)

    print(stochastic_local_search(g, 10000))




