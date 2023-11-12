import networkx as nx
from time import time_ns
import random
import numpy as np


def generate_dag(num_vertices, num_edges):
    complete_graph = nx.complete_graph(num_vertices, create_using=nx.DiGraph)
    edges = list(complete_graph.edges())
    random.shuffle(edges)

    G = nx.DiGraph()
    G.add_nodes_from(range(num_vertices))

    for edge in edges[:num_edges]:
        G.add_edge(*edge)

    random.shuffle(edges)

    while not nx.is_directed_acyclic_graph(G):
        edges_to_remove = list(nx.find_cycle(G))
        G.remove_edges_from(edges_to_remove)

    remaining_edges = list(G.edges())
    return G, len(remaining_edges)


def main():
    min_vertices = 100   # Минимальное количество вершин в графе
    max_vertices = 1000  # Максимальное количество вершин в графе
    step = 100           # Шаг по количеству вершин
    repetitions = 100    # Количество сгенерированных графов

    for num_vertices in range(min_vertices, max_vertices + 1, step):
        max_edges = num_vertices * (num_vertices - 1) // 2  # Максимальное количество ребер в графе
        step_edges = (max_edges - num_vertices) // 10       # Шаг по количеству ребер

        for num_edges in range(num_vertices, max_edges, step_edges):
            execution_times = []
            remaining_edges_sum = 0
            for _ in range(repetitions):
                graph, remaining_edges = generate_dag(num_vertices, num_edges)
                remaining_edges_sum += remaining_edges

                start_time = time_ns()
                nx.topological_sort(graph)
                end_time = time_ns()

                execution_time = end_time - start_time
                execution_times.append(execution_time)

            remaining_edges_average = remaining_edges_sum / repetitions
            execution_times.sort()
            quantile_20 = int(0.20 * repetitions)
            quantile_80 = int(0.80 * repetitions)
            selected_times = execution_times[quantile_20:quantile_80]
            average_time = np.mean(selected_times)

            print(f"Vertices: {num_vertices}, Edges: {num_edges}, Average Remaining Edges: {remaining_edges_average:.2f}, Average Execution Time: {average_time} ns")


if __name__ == "__main__":
    main()

