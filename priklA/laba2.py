import time
from collections import deque
import csv

def load_graph_from_csv(filename):
    graph = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            node = int(row[0])
            neighbors = list(map(int, row[1:]))
            graph[node] = neighbors
    return graph

# (DFS)
def dfs(graph, start):
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)

            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
    return result

# (BFS)
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            result.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return result

# время работы обхода
def measure_time(graph, start, traversal_type):
    start_time = time.time()

    if traversal_type == 'dfs':
        result = dfs(graph, start)
    elif traversal_type == 'bfs':
        result = bfs(graph, start)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Результат обхода ({traversal_type}): {result}")
    print(f"Время выполнения {traversal_type.upper()}: {elapsed_time:.6f} секунд")
    return result, elapsed_time


graph = load_graph_from_csv('graph.csv')

start_vertex = 0

bfs_result, bfs_time = measure_time(graph, start_vertex, 'bfs')
dfs_result, dfs_time = measure_time(graph, start_vertex, 'dfs')
