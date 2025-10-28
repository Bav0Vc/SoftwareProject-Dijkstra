"""
Generate dynamic Dijkstra exercises for JACK3 using a 5-city European graph.

Requirements:
- pip install graphviz Pillow
- Helper modules in the same folder:
  - append_question_number_to_string.py
  - formatter_for_copy_paste_export_to_jack3.py
  - formatter_to_xml.py
"""

from datetime import datetime
import random
import base64
import graphviz as gv
import heapq

# Helper modules
from append_question_number_to_string import append_question_number_to_string
from formatter_for_copy_paste_export_to_jack3 import format_list_of_strings, format_list_of_values
from formatter_to_xml import format_to_xml, clear_variable_declarations, format_images_to_xml, clear_resources

# Cities
CITIES = ["Berlin", "Paris", "London", "Prague", "Vienna"]

# Random graph generator
def generate_graph(cities, rng):
    edges = []
    # Ensure some connectivity (not fully circular)
    for i in range(len(cities)):
        for j in range(i+1, len(cities)):
            if rng.random() < 0.5:  # 50% chance of edge
                weight = rng.randint(1, 10)
                edges.append((cities[i], cities[j], weight))
                edges.append((cities[j], cities[i], weight))
    return edges

# Dijkstra implementation
def dijkstra(nodes, edges, source, target):
    graph = {n: [] for n in nodes}
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = {n: float("inf") for n in nodes}
    dist[source] = 0
    prev = {n: None for n in nodes}

    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == target:
            break
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    # Reconstruct path
    path = []
    u = target
    while u:
        path.insert(0, u)
        u = prev[u]
    return dist[target], path

# Render graph image
def render_graph_image(nodes, edges, path_nodes, title):
    dot = gv.Digraph("graph")
    dot.attr("graph", dpi="150", rankdir="LR", label=title, labelloc="t")
    dot.attr("node", shape="circle", style="filled", fillcolor="white")
    dot.attr("edge", arrowsize="0.8")

    path_edges = set(zip(path_nodes, path_nodes[1:]))

    for n in nodes:
        fill = "white"
        if n == path_nodes[0]:
            fill = "palegreen"
        elif n == path_nodes[-1]:
            fill = "lightyellow"
        elif n in path_nodes:
            fill = "lightblue"
        dot.node(n, n, fillcolor=fill)

    for u, v, w in edges:
        if (u, v) in path_edges:
            dot.edge(u, v, label=str(w), color="royalblue", penwidth="2.5")
        else:
            dot.edge(u, v, label=str(w))

    png_bytes = dot.pipe(format="png")
    return base64.b64encode(png_bytes).decode("utf-8")

# Build N instances of exercises
def build_instances(question_number: int, num_instances=3, seed=123):
    rng = random.Random(seed)

    nodes_all, edges_all, sources_all, targets_all = [], [], [], []
    dists_all, paths_all = [], []
    imgb64_all, imgdatauri_all = [], []
    images = []

    source = rng.choice(CITIES)
    target = rng.choice([c for c in CITIES if c != source])

    for i in range(num_instances):
        edges = generate_graph(CITIES, rng)
        dist, path = dijkstra(CITIES, edges, source, target)

        nodes_all.append(",".join(CITIES))
        edges_all.append(";".join(f"{u},{v},{w}" for u,_
