import heapq

def dijkstra(graph, source):
    """
    graph: dict of {node: [(neighbor, weight), ...]}
    source: starting node
    Returns: dict of {node: shortest_distance_from_source}
    """
    # Step 1: initialize distances to infinity, except source = 0
    distances = {node: float('inf') for node in graph}
    distances[source] = 0

    # Step 2: min-heap of (distance, node), start with the source
    min_heap = [(0, source)]

    # Step 3: track finalized (visited) nodes
    visited = set()

    while min_heap:
        current_dist, current_node = heapq.heappop(min_heap)

        # Case: stale entry (we already found a better path earlier) -> skip
        if current_node in visited:
            continue
        visited.add(current_node)

        # Relax all neighbors
        for neighbor, weight in graph[current_node]:
            if weight < 0:
                raise ValueError("Dijkstra does not support negative weights.")

            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(min_heap, (new_dist, neighbor))

    return distances


if __name__ == "__main__":
    # Undirected graph example (add both directions)
    graph = {
        'A': [('B', 4), ('C', 1)],
        'B': [('A', 4), ('D', 2)],
        'C': [('A', 1), ('D', 5)],
        'D': [('B', 2), ('C', 5)],
        'E': []  # disconnected node, unreachable from A
    }

    result = dijkstra(graph, 'A')

    for node, dist in result.items():
        if dist == float('inf'):
            print(f"{node}: unreachable")
        else:
            print(f"{node}: {dist}")