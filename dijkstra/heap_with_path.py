import heapq

def dijkstra_with_path(graph, source):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    previous = {node: None for node in graph}
    min_heap = [(0, source)]
    visited = set()

    while min_heap:
        current_dist, current_node = heapq.heappop(min_heap)
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, weight in graph[current_node]:
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(min_heap, (new_dist, neighbor))

    return distances, previous

def reconstruct_path(previous, target):
    path = []
    while target is not None:
        path.append(target)
        target = previous[target]
    return path[::-1]  # reverse to get source -> target order

# Usage:
# distances, previous = dijkstra_with_path(graph, 'A')
# print(reconstruct_path(previous, 'D'))   # e.g. ['A', 'C', 'D'] or ['A','B','D']