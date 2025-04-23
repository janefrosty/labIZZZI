import heapq
import sys
from typing import List, Dict, Tuple, Optional


class Graph:
    def __init__(self, vertices: int):
        self.V = vertices
        self.graph: List[Dict[int, int]] = [{} for _ in range(vertices)]

    def add_edge(self, u: int, v: int, w: int):
        self.graph[u][v] = w

    def dijkstra(self, src: int, dest: int) -> Optional[Tuple[List[int], int]]:
        # Проверка на отрицательные веса
        for u in range(self.V):
            for v, w in self.graph[u].items():
                if w < 0:
                    print("Граф содержит ребра с отрицательным весом!")
                    return None

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        prev = [-1] * self.V
        visited = [False] * self.V

        heap = []
        heapq.heappush(heap, (0, src))

        while heap:
            current_dist, u = heapq.heappop(heap)

            if u == dest:
                break

            if visited[u]:
                continue
            visited[u] = True

            for v, weight in self.graph[u].items():
                if not visited[v] and dist[v] > dist[u] + weight:
                    dist[v] = dist[u] + weight
                    prev[v] = u
                    heapq.heappush(heap, (dist[v], v))

        if dist[dest] == sys.maxsize:
            print(f"Путь от вершины {src} до вершины {dest} не существует")
            return None

        path = []
        current = dest
        while current != -1:
            path.append(current)
            current = prev[current]
        path.reverse()

        return path, dist[dest]

    def has_negative_cycle(self) -> bool:
        dist = [0] * self.V

        # Релаксация всех ребер V-1 раз
        for _ in range(self.V - 1):
            for u in range(self.V):
                for v, w in self.graph[u].items():
                    if dist[u] != sys.maxsize and dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w

        # Проверка на отрицательные циклы
        for u in range(self.V):
            for v, w in self.graph[u].items():
                if dist[u] != sys.maxsize and dist[v] > dist[u] + w:
                    return True
        return False


def read_graph_from_file(filename: str) -> Graph:
    """Читает граф из файла"""
    with open(filename, 'r') as f:
        lines = f.readlines()
        V, E = map(int, lines[0].split())
        graph = Graph(V)
        for line in lines[1:E + 1]:
            u, v, w = map(int, line.split())
            graph.add_edge(u, v, w)
    return graph


def write_graph_to_file(filename: str, graph: Graph):
    """Записывает граф в файл"""
    with open(filename, 'w') as f:
        # Подсчет количества ребер
        E = sum(len(edges) for edges in graph.graph)
        f.write(f"{graph.V} {E}\n")
        for u in range(graph.V):
            for v, w in graph.graph[u].items():
                f.write(f"{u} {v} {w}\n")


def main():
    # Создаем тестовый граф и записываем его в файл
    input_filename = "graph.txt"
    output_filename = "shortest_path.txt"

    # Пример графа (можно заменить на любой другой)
    g = Graph(5)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 1)
    g.add_edge(1, 3, 1)
    g.add_edge(2, 1, 2)
    g.add_edge(2, 3, 5)
    g.add_edge(3, 4, 3)

    # Записываем граф в файл
    write_graph_to_file(input_filename, g)

    # Читаем граф из файла
    graph = read_graph_from_file(input_filename)

    # Проверка на отрицательные циклы
    if graph.has_negative_cycle():
        print("Граф содержит отрицательный цикл!")
        return

    # Находим кратчайший путь от 0 до 4
    src = 0
    dest = 4
    result = graph.dijkstra(src, dest)

    if result:
        path, distance = result
        print(f"Кратчайший путь от вершины {src} до вершины {dest}: {' -> '.join(map(str, path))}")
        print(f"Длина пути: {distance}")

        # Записываем результат в файл
        with open(output_filename, 'w') as f:
            f.write(f"Кратчайший путь от вершины {src} до вершины {dest}:\n")
            f.write(' -> '.join(map(str, path)) + "\n")  # Исправлено: добавлена закрывающая скобка
            f.write(f"Длина пути: {distance}\n")
    else:
        print(f"Путь от вершины {src} до вершины {dest} не существует")


if __name__ == "__main__":
    main()