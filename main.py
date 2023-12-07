from bnb_dfs import *

if __name__ == '__main__':
    g = read_graph("10_0.0_1.0.out")
    solution = BranchAndBoundDfs(g)
    solution.solve(Path([], graph=g), {x for x in range(0, len(g))})
    print(solution.best_path)



