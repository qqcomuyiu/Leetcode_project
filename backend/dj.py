import heapq
import copy
from collections import defaultdict

def convert_to_desired_format(old_graph):
    new_graph = {}
    for key, value_list in old_graph.items():
        new_graph[key] = {item[0]: item[1] for item in value_list}
    return new_graph

class Dijkstra:
    def __init__(self, graph):
        """
        Initialize the Dijkstra algorithm class.
        """
        self.original_graph = copy.deepcopy(graph)  # Save a deep copy of the original graph
        self.graph = graph

    def find_shortest_path(self, start_vertex, end_vertex):
        """
        Use the Dijkstra algorithm to find the shortest path and its length from start_vertex to end_vertex.
        """
        distances = {vertex: float('infinity') for vertex in self.graph}
        previous_vertices = {vertex: None for vertex in self.graph}
        distances[start_vertex] = 0
        pq = [(0, start_vertex)]

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_vertex == end_vertex:
                break

            for neighbor, weight in self.graph[current_vertex].items():
                distance = float(current_distance) + float(weight)
                if neighbor in distances:
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_vertices[neighbor] = current_vertex
                        heapq.heappush(pq, (distance, neighbor))

        return distances[end_vertex], self._get_path(previous_vertices, end_vertex)

    def _get_path(self, previous_vertices, end_vertex):
        """
        Backtrace the shortest path from end_vertex to start_vertex using previous_vertices.
        """
        path = []
        current_vertex = end_vertex
        while current_vertex is not None:
            path.append(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        path.reverse()
        return path

    def update_graph_for_delays(self, delayed_routes, delay_time):
        """
        Update the graph to reflect train delays.
        """
        for route in delayed_routes:
            if route in self.graph:
                for destination in self.graph[route]:
                    self.graph[route][destination] += delay_time

    def remove_station(self, station):
        """
        Remove a station and its related edges from the graph.
        """
        if station in self.graph:
            del self.graph[station]
        for source in self.graph:
            if station in self.graph[source]:
                del self.graph[source][station]

    def restore_graph(self):
        """
        Restore the graph to its original state.
        """
        self.graph = copy.deepcopy(self.original_graph)

# Example usage
'''
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

dijkstra = Dijkstra(graph)
# Assume the train from B to D is delayed, adding a 10-minute delay
dijkstra.update_graph_for_delays([('B', 'D')], 10)
# Assume station C is not serviced today, remove station C
dijkstra.remove_station('C')

path_length, path = dijkstra.find_shortest_path('A', 'D')
print(f"Shortest path length from A to D: {path_length}")
print(f"Shortest path from A to D: {path}")

# Restore the graph to its original state
dijkstra.restore_graph()

# Find the shortest path again, now the graph has been restored to its original state
path_length, path = dijkstra.find_shortest_path('A', 'D')
'''