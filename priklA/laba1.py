import random
import csv

#генерим граф
class Graph:
    def __init__(self, num_vertices, directed=False, weighted=False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.weighted = weighted
        self.graph = {i: [] for i in range(num_vertices)}

    def generate_random_graph(self, connectivity_factor=0.3): #плотность рёберышек (0 или 1)
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if random.random() < connectivity_factor: #генерим ребрышки в зависимости от их плотности
                    weight = random.randint(1, 10) if self.weighted else None
                    self.add_edge(i, j, weight)
                    if not self.directed: #условие, если граф не ориентированный
                        self.add_edge(j, i, weight)

    def add_edge(self, u, v, weight=None):
        if weight is not None:
            self.graph[u].append((v, weight))
        else:
            self.graph[u].append(v)

    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for u in range(self.num_vertices):
                row = [u] + [f"{v},{w}" if isinstance(v, tuple) else str(v) for v, w in self.graph[u]]
                writer.writerow(row)

    def print_graph(self):
        for u in range(self.num_vertices):
            print(f"Вершина {u}: {self.graph[u]}")


# Пример использования
num_vertices = 10
connectivity_factor = 0.2
directed = False
weighted = True

graph = Graph(num_vertices, directed, weighted)

graph.generate_random_graph(connectivity_factor)

graph.print_graph()

graph.save_to_csv("graph.csv")
