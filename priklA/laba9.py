import random
from collections import defaultdict


class EdgeColoring:
    def __init__(self):
        self.graph = defaultdict(list)
        self.edges = []
        self.edge_colors = {}
        self.node_degree = defaultdict(int)
        self.max_degree = 0

    def read_graph_from_file(self, filename): # для csv формата
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    if ',' in line:
                        parts = line.strip().split(',')
                    else:
                        parts = line.strip().split()

                    if len(parts) >= 2:
                        try:
                            u, v = map(int, parts[:2])
                            self.add_edge(u, v)
                        except ValueError:
                            print(f"Пропуск строки с неверным форматом: {line.strip()}")

    def add_edge(self, u, v):
        if u > v:  # для избежания дублирования ребер (u,v) и (v,u)
            u, v = v, u
        if (u, v) not in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
            self.edges.append((u, v))
            self.node_degree[u] += 1
            self.node_degree[v] += 1
            if self.node_degree[u] > self.max_degree:
                self.max_degree = self.node_degree[u]
            if self.node_degree[v] > self.max_degree:
                self.max_degree = self.node_degree[v]

    def greedy_edge_coloring(self):
        for u, v in self.edges:
            used_colors = set()
            for neighbor in self.graph[u]:
                if (u, neighbor) in self.edge_colors:
                    used_colors.add(self.edge_colors[(u, neighbor)])
                elif (neighbor, u) in self.edge_colors:
                    used_colors.add(self.edge_colors[(neighbor, u)])
            for neighbor in self.graph[v]:
                if (v, neighbor) in self.edge_colors:
                    used_colors.add(self.edge_colors[(v, neighbor)])
                elif (neighbor, v) in self.edge_colors:
                    used_colors.add(self.edge_colors[(neighbor, v)])
            available_color = 1
            while available_color in used_colors:
                available_color += 1
            self.edge_colors[(u, v)] = available_color

    def save_coloring_to_file(self, filename):
        with open(filename, 'w') as file:
            for edge, color in self.edge_colors.items():
                file.write(f"{edge[0]} {edge[1]} {color}\n")

    def generate_random_graph(self, filename, num_nodes, num_edges):
        if num_edges > num_nodes * (num_nodes - 1) // 2:
            print(f"Ошибка: для {num_nodes} вершин максимальное количество ребер: {num_nodes * (num_nodes - 1) // 2}")
            return False

        edges = set()
        possible_edges = [(u, v) for u in range(1, num_nodes + 1)
                          for v in range(u + 1, num_nodes + 1)]

        if num_edges > len(possible_edges):
            num_edges = len(possible_edges)

        edges = random.sample(possible_edges, num_edges)

        with open(filename, 'w') as file:
            for u, v in edges:
                file.write(f"{u} {v}\n")
        return True


def main():
    print("Программа для реберной раскраски графов")
    print("1. Сгенерировать случайный граф")
    print("2. Произвести реберную раскраску графа из файла")
    choice = input("Выберите действие (1/2): ")

    edge_coloring = EdgeColoring()

    if choice == '1':
        num_nodes = int(input("Введите количество вершин: "))
        num_edges = int(input("Введите количество ребер: "))
        input_file = "random_graph.txt"
        if not edge_coloring.generate_random_graph(input_file, num_nodes, num_edges):
            return
        print(f"Сгенерированный граф сохранен в файл {input_file}")
    elif choice == '2':
        input_file = input("Введите имя файла с графом: ")
    else:
        print("Неверный выбор")
        return

    # чтение графа
    try:
        edge_coloring.read_graph_from_file(input_file)
    except FileNotFoundError:
        print(f"Файл {input_file} не найден")
        return

    print(f"Граф содержит {len(edge_coloring.graph)} вершин и {len(edge_coloring.edges)} ребер")
    print(f"Максимальная степень вершины: {edge_coloring.max_degree}")

    print("Выполняется реберная раскраска...")
    edge_coloring.greedy_edge_coloring()

    output_file = "edge_coloring.txt"
    edge_coloring.save_coloring_to_file(output_file)
    print(f"Результат раскраски сохранен в файл {output_file}")

    used_colors = set(edge_coloring.edge_colors.values())
    print(f"Использовано {len(used_colors)} цветов")
    print(f"Теоретическая верхняя граница: {edge_coloring.max_degree + 1} цветов")


if __name__ == "__main__":
    main()