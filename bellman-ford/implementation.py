def bellman_ford(num_vertices, edges, source):
    """
    num_vertices: total number of nodes, labeled 0 .. num_vertices-1
    edges: list of (u, v, weight) tuples
    source: starting node
    Returns: list of shortest distances, OR None if a negative cycle
             reachable from the source is detected.
    """
    INF = float('inf')
    dist = [INF] * num_vertices
    dist[source] = 0

    # Step 1: relax all edges (V - 1) times
    for i in range(num_vertices - 1):
        updated = False
        for u, v, weight in edges:
            if dist[u] != INF and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                updated = True
        # Optimization: if nothing changed in a full pass, we've
        # already converged and can stop early.
        if not updated:
            break

    # Step 2: one extra pass to detect a negative cycle
    for u, v, weight in edges:
        if dist[u] != INF and dist[u] + weight < dist[v]:
            return None  # negative cycle reachable from source

    return dist


if __name__ == "__main__":
    V = 5
    # (from, to, weight)
    edges = [
        (0, 1, 5),
        (1, 2, 1),
        (1, 3, 2),
        (2, 4, 1),
        (4, 3, -1),
    ]

    result = bellman_ford(V, edges, source=0)

    if result is None:
        print("Negative weight cycle detected — shortest paths undefined.")
    else:
        for node, d in enumerate(result):
            print(f"{node}: {'unreachable' if d == float('inf') else d}")
