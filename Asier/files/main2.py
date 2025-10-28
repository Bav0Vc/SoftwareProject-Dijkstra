"""
Generate N (default 3) Graph tasks for JACK3 with dynamic images.
5 random cities with random connections and weights.

Requirements:
- pip install graphviz Pillow
- Helper modules in the same folder:
  - append_question_number_to_string.py
  - formatter_for_copy_paste_export_to_jack3.py
  - formatter_to_xml.py
  - Example Exercise XML to write to
"""

from datetime import datetime
import random
import base64
import graphviz as gv

# Helper modules (existing files in your project)
from append_question_number_to_string import append_question_number_to_string
from formatter_for_copy_paste_export_to_jack3 import format_list_of_strings, format_list_of_values
from formatter_to_xml import format_to_xml, clear_variable_declarations, format_images_to_xml, clear_resources

# Render a single city graph image
def render_graph_image(nodes, edges, path_nodes, source, target):
    dot = gv.Digraph("city_dijkstra")
    dot.attr("graph", dpi="150", rankdir="LR", 
             label=f"Dijkstra – shortest path from {source} to {target}", 
             labelloc="t")
    dot.attr("node", shape="circle", style="filled", fillcolor="white")
    dot.attr("edge", arrowsize="0.8")

    on_path = set(path_nodes)
    for n in nodes:
        fill = "white"
        if n == path_nodes[0]:
            fill = "palegreen"     # start
        elif n == path_nodes[-1]:
            fill = "lightyellow"   # target
        elif n in on_path:
            fill = "lightblue"     # on shortest path
        dot.node(n, n, fillcolor=fill)

    path_edges = set(zip(path_nodes, path_nodes[1:]))

    for (u, v, w) in edges:
        if (u, v) in path_edges:
            dot.edge(u, v, label=str(w), color="royalblue", penwidth="2.6")
        else:
            dot.edge(u, v, label=str(w))

    png_bytes = dot.pipe(format="png")
    return base64.b64encode(png_bytes).decode("utf-8")

# Simple Dijkstra implementation
def dijkstra(nodes, edges, source, target):
    # Build adjacency list
    graph = {n: [] for n in nodes}
    for (u, v, w) in edges:
        graph[u].append((v, w))
    
    # Initialize distances and previous nodes
    dist = {n: float('inf') for n in nodes}
    prev = {n: None for n in nodes}
    dist[source] = 0
    unvisited = set(nodes)
    
    while unvisited:
        # Find node with minimum distance
        current = min(unvisited, key=lambda n: dist[n])
        
        if dist[current] == float('inf') or current == target:
            break
            
        unvisited.remove(current)
        
        # Update distances to neighbors
        for neighbor, weight in graph[current]:
            alt = dist[current] + weight
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current
    
    # Reconstruct path
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = prev[current]
    
    return path, dist[target]

# Generate random city graph
def generate_random_city_graph(cities, rng, wmin=1, wmax=15, connectivity=0.5):
    """
    Generate random edges between cities.
    connectivity: probability that an edge exists between two cities
    """
    edges = []
    
    # Ensure graph is connected by creating a spanning tree first
    shuffled = cities.copy()
    rng.shuffle(shuffled)
    for i in range(len(shuffled) - 1):
        weight = rng.randint(wmin, wmax)
        edges.append((shuffled[i], shuffled[i+1], weight))
    
    # Add additional random edges
    for i, city1 in enumerate(cities):
        for city2 in cities[i+1:]:
            # Skip if edge already exists
            if any((u == city1 and v == city2) or (u == city2 and v == city1) 
                   for (u, v, _) in edges):
                continue
            
            if rng.random() < connectivity:
                weight = rng.randint(wmin, wmax)
                edges.append((city1, city2, weight))
    
    return edges

# Build variables & images for k instances
def build_city_instances(question_number: int, k: int = 3, seed: int | None = 123):
    rng = random.Random(seed)
    
    # Pool of city names
    CITY_POOL = [
        "Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao",
        "Málaga", "Zaragoza", "Murcia", "Granada", "Córdoba",
        "Alicante", "Valladolid", "Vigo", "Gijón", "Toledo"
    ]

    nodes_all = []        # ["Madrid,Barcelona,Valencia,Sevilla,Bilbao", ...]
    edges_all = []        # ["Madrid,Barcelona,5;Barcelona,Valencia,3;...", ...]
    sources_all = []      # ["Madrid", ...]
    targets_all = []      # ["Valencia", ...]
    dists_all = []        # [shortest distance, ...]
    paths_all = []        # ["Madrid,Barcelona,Valencia", ...]
    imgb64_all = []       # pure base64 per instance
    imgdatauri_all = []   # 'data:image/png;base64,<b64>' per instance
    images = []           # resources: (filename, base64, iso_timestamp)

    for i in range(k):
        # Select 5 random cities for this instance
        cities = rng.sample(CITY_POOL, 5)
        
        # Generate random graph
        edges = generate_random_city_graph(cities, rng, wmin=1, wmax=15, connectivity=0.4)
        
        # Pick random source and target
        source, target = rng.sample(cities, 2)
        
        # Calculate shortest path
        shortest_path, shortest_dist = dijkstra(cities, edges, source, target)

        # strings for JACK3 lists
        nodes_all.append(",".join(cities))
        edges_all.append(";".join([f"{u},{v},{w}" for (u, v, w) in edges]))
        sources_all.append(source)
        targets_all.append(target)
        dists_all.append(shortest_dist)
        paths_all.append(",".join(shortest_path))

        # image (both as resource and as variables)
        img_b64 = render_graph_image(
            cities, edges, shortest_path, source, target
        )
        filename = f"dijkstra_{question_number}_{i+1}.png"
        ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        images.append((filename, img_b64, ts))
        imgb64_all.append(img_b64)
        imgdatauri_all.append(f"data:image/png;base64,{img_b64}")

    # variable names with question suffix
    def N(name): return append_question_number_to_string(question_number, name)

    # assemble JACK3 list strings
    nodes_str     = "list(" + ", ".join([f"'{s}'" for s in nodes_all]) + ")"
    edges_str     = "list(" + ", ".join([f"'{s}'" for s in edges_all]) + ")"
    sources_str   = format_list_of_strings(sources_all)
    targets_str   = format_list_of_strings(targets_all)
    dists_str     = format_list_of_values(dists_all)
    paths_str     = "list(" + ", ".join([f"'{s}'" for s in paths_all]) + ")"
    imgb64_str    = "list(" + ", ".join([f"'{b64}'" for b64 in imgb64_all]) + ")"
    imgdatauri_str= "list(" + ", ".join([f"'{uri}'" for uri in imgdatauri_all]) + ")"

    # JACK3 variable triplets: (list_var_name, single_var_name, list_value_string)
    name_input_array = [
        (N('nodes'),         N('nodes_single'),         nodes_str),
        (N('edges'),         N('edges_single'),         edges_str),
        (N('sources'),       N('source'),               sources_str),
        (N('targets'),       N('target'),               targets_str),
        (N('distances'),     N('distance'),             dists_str),
        (N('shortestpaths'), N('shortestpath'),         paths_str),
        (N('imgb64s'),       N('imgb64'),               imgb64_str),      # raw base64
        (N('imgdatauris'),   N('imgdatauri'),           imgdatauri_str),  # ready-to-use data URIs
    ]

    return name_input_array, images, k

# Write to existing Exercise XML
if __name__ == "__main__":
    # Set the folder that contains exactly ONE Exercise XML
    folder_path = r"path_to_your_resources"   # <-- adjust
    question_number = 7
    seed = 123
    num_instances = 3

    # Clear previous variables/resources
    clear_variable_declarations(folder_path)
    clear_resources(folder_path)

    # Build variables + images
    name_input_array, image_input_array, question_amount = build_city_instances(
        question_number=question_number,
        k=num_instances,
        seed=seed
    )

    # Write variables (includes imgb64s/imgb64 and imgdatauris/imgdatauri)
    format_to_xml(folder_path, name_input_array, question_number, question_amount)

    # Also add images as ExerciseResources
    format_images_to_xml(folder_path, image_input_array)

    print(f"Generated {question_amount} city Dijkstra tasks with dynamic images.")
