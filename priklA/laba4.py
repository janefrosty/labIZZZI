import csv


def read_graph(file_name):

    graph = {}
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            vertex = int(row[0])  # колонка - вершина
            neighbors = list(map(int, row[1:]))  # соседи
            graph[vertex] = neighbors
    return graph


def dfs(graph, vertex, visited):

    stack = [vertex]
    component = []
    visited.add(vertex)

    while stack:
        node = stack.pop()
        component.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return component


def find_connected_components(graph):

    visited = set()
    components = []

    for vertex in graph:
        if vertex not in visited:
            component = dfs(graph, vertex, visited)
            components.append(component)

    return components


def extract_largest_component(components):

    largest_component = max(components, key=len)
    return largest_component


def write_graph(file_name, component, graph):

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        for vertex in component:
            #вершины, которые принадлежат компоненте
            neighbors = [neighbor for neighbor in graph[vertex] if neighbor in component]
            writer.writerow([vertex] + neighbors)


def main(input_file, output_file):

    graph = read_graph(input_file)

    components = find_connected_components(graph)
    # максимальная компоненты
    largest_component = extract_largest_component(components)

    write_graph(output_file, largest_component, graph)


if __name__ == "__main__":
    input_file = "graph.csv"
    output_file = "largest_component.csv"
    main(input_file, output_file)
