import numpy as np
from collections import deque


class HungarianAlgorithm:
    def __init__(self, adjacency_matrix):

        self.adjacency_matrix = adjacency_matrix
        self.left_size = len(adjacency_matrix)
        self.right_size = len(adjacency_matrix[0]) if self.left_size > 0 else 0

        # инициализация паросочетаний
        self.pair_U = [-1] * self.left_size  # для левой доли
        self.pair_V = [-1] * self.right_size  # для правой доли
        self.dist = [0] * self.left_size

    def bfs(self):
        queue = deque()

        for u in range(self.left_size):
            if self.pair_U[u] == -1:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float('inf')

        self.dist_null = float('inf')

        while queue:
            u = queue.popleft()

            if self.dist[u] < self.dist_null:
                for v in range(self.right_size):
                    if self.adjacency_matrix[u][v]:
                        if self.pair_V[v] == -1:
                            self.dist_null = self.dist[u] + 1
                        elif self.dist[self.pair_V[v]] == float('inf'):
                            self.dist[self.pair_V[v]] = self.dist[u] + 1
                            queue.append(self.pair_V[v])

        return self.dist_null != float('inf')

    def dfs(self, u):

        for v in range(self.right_size):
            if self.adjacency_matrix[u][v]:
                if self.pair_V[v] == -1 or (self.dist[self.pair_V[v]] == self.dist[u] + 1 and self.dfs(self.pair_V[v])):
                    self.pair_U[u] = v
                    self.pair_V[v] = u
                    return True
        self.dist[u] = float('inf')
        return False

    def maximum_matching(self):

        result = 0

        while self.bfs():
            for u in range(self.left_size):
                if self.pair_U[u] == -1:
                    if self.dfs(u):
                        result += 1

        matching = []
        for u in range(self.left_size):
            if self.pair_U[u] != -1:
                matching.append((u, self.pair_U[u]))

        return matching


def test_hungarian():
    # тестовый граф чтоб работала прога
    adjacency_matrix = [
        [1, 0, 1],
        [1, 1, 0],
        [0, 1, 0]
    ]

    hungarian = HungarianAlgorithm(adjacency_matrix)
    matching = hungarian.maximum_matching()

    print("Максимальное паросочетание:", matching)
    print("Размер паросочетания:", len(matching))


if __name__ == "__main__":
    test_hungarian()