import numpy as np
import random


def generate_bipartite_graph(left_size, right_size, density=0.3, filename='bipartite_graph.txt'):

    # матрица смежности
    adjacency_matrix = np.zeros((left_size, right_size), dtype=int)

    # случайные ребра
    for i in range(left_size):
        for j in range(right_size):
            if random.random() < density:
                adjacency_matrix[i][j] = 1

    with open(filename, 'w') as f:
        f.write(f"{left_size} {right_size}\n")

        for i in range(left_size):
            row = ' '.join(map(str, adjacency_matrix[i]))
            f.write(row + '\n')

    print(f"Двудольный граф с {left_size} левыми и {right_size} правыми вершинами сохранен в {filename}")


def read_bipartite_graph(filename='bipartite_graph.txt'):

    with open(filename, 'r') as f:
        left_size, right_size = map(int, f.readline().split())

        adjacency_matrix = []
        for _ in range(left_size):
            row = list(map(int, f.readline().split()))
            adjacency_matrix.append(row)

    return left_size, right_size, adjacency_matrix


if __name__ == "__main__":
    generate_bipartite_graph(10, 10, 0.5)