import time
from graph_generator import generate_bipartite_graph, read_bipartite_graph
from hungarian import HungarianAlgorithm


def main():
    # параметры графа
    left_size = 2000
    right_size = 2000
    density = 0.1

    print(f"Генерация двудольного графа с {left_size} и {right_size} вершинами...")
    generate_bipartite_graph(left_size, right_size, density, 'large_bipartite_graph.txt')

    print("Чтение графа из файла...")
    left_size, right_size, adjacency_matrix = read_bipartite_graph('large_bipartite_graph.txt')

    print("Поиск максимального паросочетания...")
    start_time = time.time()

    hungarian = HungarianAlgorithm(adjacency_matrix)
    matching = hungarian.maximum_matching()

    end_time = time.time()

    print(f"Найдено паросочетание размером {len(matching)}")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")

    with open('matching_result.txt', 'w') as f:
        f.write(f"Размер паросочетания: {len(matching)}\n")
        f.write(f"Время выполнения: {end_time - start_time:.2f} секунд\n")
        f.write("Первые 10 пар паросочетания:\n")
        for pair in matching[:10]:
            f.write(f"{pair[0]} - {pair[1]}\n")


if __name__ == "__main__":
    main()