import csv


#Система непересекающихся множеств
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:

            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


# Чтение графа из файла
def read_graph(file_name):
    adj_list = {}
    edges = []
    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            node = int(row[0])
            adj_list[node] = []
            for i in range(1, len(row), 2):
                if i + 1 < len(row):
                    neighbor = int(row[i])
                    weight = int(row[i + 1])
                    adj_list[node].append((neighbor, weight))
                    edges.append((weight, node, neighbor))
    return adj_list, edges


# Алгоритм Крускала
def kruskal(n, edges):
    edges.sort()
    uf = UnionFind(n)
    mst = []

    for weight, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, weight))

    return mst


# Построение списка смежности
def build_mst_adj_list(mst):
    mst_adj_list = {}
    for u, v, weight in mst:
        if u not in mst_adj_list:
            mst_adj_list[u] = []
        if v not in mst_adj_list:
            mst_adj_list[v] = []
        mst_adj_list[u].append((v, weight))
        mst_adj_list[v].append((u, weight))
    return mst_adj_list


# Запись результата в файл
def write_graph(mst_adj_list, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for u, neighbors in mst_adj_list.items():
            row = [u]
            for v, weight in neighbors:
                row.append(v)
                row.append(weight)
            writer.writerow(row)


def main():
    input_file = 'graph.csv'
    output_file = 'mst.csv'

    adj_list, edges = read_graph(input_file)

    n = len(adj_list)

    mst = kruskal(n, edges)

    mst_adj_list = build_mst_adj_list(mst)

    write_graph(mst_adj_list, output_file)
    print(f'MST записан в {output_file}')


if __name__ == '__main__':
    main()
