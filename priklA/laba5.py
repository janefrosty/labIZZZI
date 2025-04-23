import collections
import random
import time
import os


class Edge:
    def __init__(self, to, rev, capacity):
        self.to = to
        self.rev = rev
        self.capacity = capacity


class Dinic:
    def __init__(self, n):
        self.size = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, fr, to, capacity): #ребро
        forward = Edge(to, len(self.graph[to]), capacity)
        backward = Edge(fr, len(self.graph[fr]), 0)
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def bfs_level(self, s, t, level):
        q = collections.deque()
        level[:] = [-1] * self.size
        level[s] = 0
        q.append(s)

        while q:
            v = q.popleft()
            for edge in self.graph[v]:
                if edge.capacity > 0 and level[edge.to] < 0:
                    level[edge.to] = level[v] + 1
                    q.append(edge.to)

    def dfs_flow(self, v, t, upTo, iter_, level): #блок поток
        if v == t:
            return upTo
        for i in range(iter_[v], len(self.graph[v])):
            edge = self.graph[v][i]
            if edge.capacity > 0 and level[v] < level[edge.to]:
                d = self.dfs_flow(edge.to, t, min(upTo, edge.capacity), iter_, level)
                if d > 0:
                    edge.capacity -= d
                    self.graph[edge.to][edge.rev].capacity += d
                    return d
            iter_[v] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        level = [-1] * self.size
        while True:
            self.bfs_level(s, t, level)
            if level[t] < 0:
                return flow
            iter_ = [0] * self.size
            while True:
                f = self.dfs_flow(s, t, float('inf'), iter_, level)
                if f == 0:
                    break
                flow += f
            level = [-1] * self.size


def generate_large_network(num_nodes, density=0.1):

    dinic = Dinic(num_nodes)
    source = 0
    sink = num_nodes - 1

    for i in range(num_nodes):
        for j in range(i + 1, min(i + 1 + int(num_nodes * density), num_nodes)):
            if i != j:
                capacity = random.randint(1, 100)
                dinic.add_edge(i, j, capacity)

    return dinic, source, sink


def save_network_to_file(filename, dinic, source, sink):

    with open(filename, 'w') as f:
        f.write(f"{dinic.size} {source} {sink}\n")
        for i in range(dinic.size):
            for edge in dinic.graph[i]:
                if edge.capacity > 0:
                    f.write(f"{i} {edge.to} {edge.capacity}\n")


def load_network_from_file(filename):

    with open(filename) as f:
        first_line = f.readline().split()
        num_nodes = int(first_line[0])
        source = int(first_line[1])
        sink = int(first_line[2])

        dinic = Dinic(num_nodes)
        for line in f:
            fr, to, cap = map(int, line.split())
            dinic.add_edge(fr, to, cap)

    return dinic, source, sink


def main():
    print("Программа для расчета максимального потока в транспортной сети (алгоритм Диница)")

    if not os.path.exists('network_files'):
        os.makedirs('network_files')

    while True:
        print("\nМеню:")
        print("1. Сгенерировать случайную большую сеть и сохранить в файл")
        print("2. Загрузить сеть из файла и вычислить максимальный поток")
        print("3. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            try:
                num_nodes = int(input("Введите количество узлов в сети (>=1000 для большой сети): "))
                if num_nodes < 2:
                    print("Сеть должна содержать хотя бы 2 узла (исток и сток)")
                    continue

                density = float(input("Введите плотность сети (0.01-0.5, рекомендуемое 0.1): "))
                if density <= 0 or density > 0.5:
                    print("Плотность должна быть в диапазоне (0, 0.5]")
                    continue

                filename = f"network_files/network_{num_nodes}_nodes_{density}_density.txt"

                print(f"Генерация сети с {num_nodes} узлами...")
                start_time = time.time()
                dinic, source, sink = generate_large_network(num_nodes, density)
                print(f"Сеть сгенерирована за {time.time() - start_time:.2f} секунд")

                print(f"Сохранение сети в файл {filename}...")
                save_network_to_file(filename, dinic, source, sink)
                print("Сеть успешно сохранена")

            except ValueError as e:
                print(f"Ошибка ввода: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '2':
            try:
                filename = input(
                    "Введите имя файла с сетью (например, network_files/network_1000_nodes_0.1_density.txt): ")

                print(f"Загрузка сети из файла {filename}...")
                start_time = time.time()
                dinic, source, sink = load_network_from_file(filename)
                print(f"Сеть загружена за {time.time() - start_time:.2f} секунд")
                print(f"Размер сети: {dinic.size} узлов")
                print(f"Исток: {source}, Сток: {sink}")

                print("Вычисление максимального потока...")
                start_time = time.time()
                max_flow = dinic.max_flow(source, sink)
                elapsed_time = time.time() - start_time
                print(f"Максимальный поток: {max_flow}")
                print(f"Время вычисления: {elapsed_time:.4f} секунд")

                result_filename = filename.replace('.txt', '_result.txt')
                with open(result_filename, 'w') as f:
                    f.write(f"Максимальный поток: {max_flow}\n")
                    f.write(f"Время вычисления: {elapsed_time:.4f} секунд\n")
                print(f"Результат сохранен в {result_filename}")

            except FileNotFoundError:
                print("Файл не найден")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '3':
            print("Выход из программы")
            break

        else:
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()