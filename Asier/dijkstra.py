import heapq

def dijkstra(nodes, edges, source):
    # Build adjacency list
    graph = {node: [] for node in nodes}
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # undirected graph

    # Initialize distances
    dist = {node: float('inf') for node in nodes}
    dist[source] = 0
    visited = set()
    pq = [(0, source)]
    steps = []  # record step-by-step updates

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph[u]:
            if dist[v] > d + w:
                old = dist[v]
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
                steps.append({
                    "updated_node": v,
                    "old_dist": old,
                    "new_dist": dist[v],
                    "from_node": u
                })
    return dist, steps
