import sys


def read_graph_from_file(filename):
    """Чтение графа из файла"""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Первая строка - количество вершин
        V = int(lines[0].strip())

        # Инициализация матрицы смежности
        dist = [[float('inf')] * V for _ in range(V)]
        for i in range(V):
            dist[i][i] = 0

        # Чтение ребер
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) == 3:
                u, v, w = map(int, parts)
                dist[u][v] = w
            else:
                print(f"Некорректный формат строки: {line}")

        return dist, V

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def floyd_warshall(dist, V):
    """Алгоритм Флойда-Уоршелла"""
    # Копирование матрицы
    dist = [row[:] for row in dist]

    # Основной алгоритм
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Проверка на отрицательные циклы
    has_negative_cycle = False
    for i in range(V):
        if dist[i][i] < 0:
            has_negative_cycle = True
            break

    return dist, has_negative_cycle


def save_results_to_file(filename, dist, V, has_negative_cycle):
    """Сохранение результатов в файл"""
    try:
        with open(filename, 'w') as file:
            if has_negative_cycle:
                file.write("Граф содержит отрицательный цикл!\n")
                file.write("Кратчайшие пути не определены для всех пар вершин.\n")
            else:
                file.write("Кратчайшие пути между всеми парами вершин:\n")
                for i in range(V):
                    for j in range(V):
                        if dist[i][j] == float('inf'):
                            file.write(f"{i} -> {j}: нет пути\n")
                        else:
                            file.write(f"{i} -> {j}: {dist[i][j]}\n")
        print(f"Результаты сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении результатов: {e}")


def generate_sample_graph(filename, V, edge_prob=0.7, max_weight=10):
    """Генерация случайного графа для тестирования"""
    import random
    try:
        with open(filename, 'w') as file:
            file.write(f"{V}\n")
            for i in range(V):
                for j in range(V):
                    if i != j and random.random() < edge_prob:
                        weight = random.randint(-max_weight, max_weight)
                        file.write(f"{i} {j} {weight}\n")
        print(f"Сгенерирован тестовый граф в файле {filename}")
    except Exception as e:
        print(f"Ошибка при генерации графа: {e}")


def main():
    print("Программа для поиска кратчайших путей между всеми парами вершин (алгоритм Флойда-Уоршелла)")

    # Создаем тестовый файл с графом, если его нет
    input_file = "graph.txt"
    output_file = "result.txt"

    try:
        # Проверяем, существует ли файл с графом
        with open(input_file, 'r'):
            pass
        print(f"Используется существующий файл графа {input_file}")
    except FileNotFoundError:
        # Если файла нет, создаем тестовый граф
        print(f"Файл {input_file} не найден. Создаем тестовый граф...")
        V = 5  # Количество вершин в тестовом графе
        generate_sample_graph(input_file, V)

    # Чтение графа из файла
    dist, V = read_graph_from_file(input_file)

    # Выполнение алгоритма Флойда-Уоршелла
    dist, has_negative_cycle = floyd_warshall(dist, V)

    # Сохранение результатов
    save_results_to_file(output_file, dist, V, has_negative_cycle)

    # Вывод информации о наличии отрицательных циклов
    if has_negative_cycle:
        print("Обнаружен отрицательный цикл в графе!")
    else:
        print("Отрицательных циклов не обнаружено.")

    print("Программа завершена.")


if __name__ == "__main__":
    main()