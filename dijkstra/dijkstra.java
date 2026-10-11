import java.util.*;

public class Dijkstra {

    // Edge representation: destination node + weight
    static class Edge {
        int to;
        int weight;
        Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    // Pair of (distance, node) used inside the priority queue
    static class Node implements Comparable<Node> {
        int id;
        int dist;
        Node(int id, int dist) {
            this.id = id;
            this.dist = dist;
        }
        @Override
        public int compareTo(Node other) {
            return Integer.compare(this.dist, other.dist);
        }
    }

    public static int[] dijkstra(List<List<Edge>> graph, int source, int numNodes) {
        int[] distances = new int[numNodes];
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[source] = 0;

        boolean[] visited = new boolean[numNodes];
        PriorityQueue<Node> minHeap = new PriorityQueue<>();
        minHeap.add(new Node(source, 0));

        while (!minHeap.isEmpty()) {
            Node current = minHeap.poll();

            // Case: stale entry, already finalized with a better distance -> skip
            if (visited[current.id]) {
                continue;
            }
            visited[current.id] = true;

            for (Edge edge : graph.get(current.id)) {
                if (edge.weight < 0) {
                    throw new IllegalArgumentException("Dijkstra does not support negative weights.");
                }
                if (visited[edge.to]) continue;

                int newDist = distances[current.id] + edge.weight;
                if (newDist < distances[edge.to]) {
                    distances[edge.to] = newDist;
                    minHeap.add(new Node(edge.to, newDist));
                }
            }
        }

        return distances;
    }

    public static void main(String[] args) {
        int numNodes = 5; // 0=A, 1=B, 2=C, 3=D, 4=E (disconnected)

        List<List<Edge>> graph = new ArrayList<>();
        for (int i = 0; i < numNodes; i++) {
            graph.add(new ArrayList<>());
        }

        // Undirected graph -> add both directions
        addUndirectedEdge(graph, 0, 1, 4);  // A-B
        addUndirectedEdge(graph, 0, 2, 1);  // A-C
        addUndirectedEdge(graph, 1, 3, 2);  // B-D
        addUndirectedEdge(graph, 2, 3, 5);  // C-D
        // Node 4 (E) has no edges -> stays unreachable

        int[] distances = dijkstra(graph, 0, numNodes);

        String[] labels = {"A", "B", "C", "D", "E"};
        for (int i = 0; i < numNodes; i++) {
            if (distances[i] == Integer.MAX_VALUE) {
                System.out.println(labels[i] + ": unreachable");
            } else {
                System.out.println(labels[i] + ": " + distances[i]);
            }
        }
    }

    static void addUndirectedEdge(List<List<Edge>> graph, int u, int v, int weight) {
        graph.get(u).add(new Edge(v, weight));
        graph.get(v).add(new Edge(u, weight));
    }
}
