"""
Generate 5-node Dijkstra tasks with VARIABLE shortest paths for JACK3.
Optimized version: 3 instances, no imgb64 (only data URIs).
"""

from datetime import datetime
import random
import base64
import graphviz as gv

from append_question_number_to_string import append_question_number_to_string
from formatter_for_copy_paste_export_to_jack3 import (
    format_list_of_strings,
    format_list_of_integers
)
from formatter_to_xml import (
    format_to_xml,
    format_images_to_xml,
    clear_variable_declarations,
    clear_resources
)

def render_graph_image(nodes, edges, path_nodes=None, title="Dijkstra"):
    """
    Render graph with 5 nodes.
    If path_nodes=None: all edges gray (question image)
    If path_nodes given: solution edges red (solution image)
    """
    dot = gv.Digraph(name="G", format="png", engine="dot")
    dot.attr(rankdir="LR", dpi="110")
    dot.attr(label=title, labelloc="t", fontsize="14")

    if path_nodes:
        path_set = set(path_nodes)
        for n in nodes:
            if n in path_set:
                dot.node(n, shape="circle", style="filled", fillcolor="#ffe599",
                        color="#cc7a00", fontsize="12")
            else:
                dot.node(n, shape="circle", style="filled", fillcolor="#f5f5f5",
                        color="#555555", fontsize="12")

        path_edges = set()
        for i in range(len(path_nodes) - 1):
            path_edges.add((path_nodes[i], path_nodes[i+1]))

        for u, v, w in edges:
            if (u, v) in path_edges:
                dot.edge(u, v, label=str(w), color="#cc0000", penwidth="2.4", fontcolor="#cc0000")
            else:
                dot.edge(u, v, label=str(w), color="#888888", penwidth="1.4", fontcolor="#444444")
    else:
        for n in nodes:
            dot.node(n, shape="circle", style="filled", fillcolor="#f5f5f5", color="#555555", fontsize="12")
        for u, v, w in edges:
            dot.edge(u, v, label=str(w), color="#888888", penwidth="1.4", fontcolor="#444444")

    png_bytes = dot.pipe(format="png")
    return base64.b64encode(png_bytes).decode("ascii")

def build_5node_instances(question_number, k, seed):
    """
    Build k instances with 5 nodes: A -> ? -> ? -> E
    Variable shortest paths for variety.
    """
    rnd = random.Random(seed) if seed is not None else random.Random()

    name_input_array = []
    image_input_array = []
    question_amount = k

    NODES = ["A", "B", "C", "D", "E"]
    SOURCE = "A"
    TARGET = "E"

    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()

    possible_paths = [
        ["A", "B", "C", "D", "E"],  # Full path
        ["A", "C", "D", "E"],        # Skip B
        ["A", "B", "D", "E"],        # Skip C
        ["A", "B", "C", "E"],        # Skip D
    ]

    for inst_num in range(k):
        SHORTEST_PATH = rnd.choice(possible_paths)

        base_weights = {}
        for i in range(len(NODES) - 1):
            u, v = NODES[i], NODES[i+1]
            base_weights[(u, v)] = rnd.randint(3, 7)

        path_cost = 0
        path_edges = set()
        for i in range(len(SHORTEST_PATH) - 1):
            u, v = SHORTEST_PATH[i], SHORTEST_PATH[i+1]
            path_edges.add((u, v))
            if (u, v) in base_weights:
                path_cost += base_weights[(u, v)]
            else:
                w = rnd.randint(4, 9)
                base_weights[(u, v)] = w
                path_cost += w

        DISTANCE = path_cost

        all_edges_pairs = [
            ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"),
            ("B", "C"), ("B", "D"), ("B", "E"),
            ("C", "D"), ("C", "E"),
            ("D", "E")
        ]

        EDGES = []
        for u, v in all_edges_pairs:
            if (u, v) in path_edges:
                w = base_weights.get((u, v), rnd.randint(3, 7))
            else:
                w = path_cost + rnd.randint(2, 8)
            EDGES.append((u, v, w))

        nodes_str = ",".join(NODES)
        edges_str = "".join([f"{u},{v},{w}" for u, v, w in EDGES])
        path_str = ",".join(SHORTEST_PATH)
        dist_str = str(DISTANCE)

        # Question image (no solution)
        img_question_b64 = render_graph_image(NODES, EDGES, path_nodes=None,
                                               title=f"Find shortest path from {SOURCE} to {TARGET}")
        img_question_uri = f"data:image/png;base64,{img_question_b64}"

        # Solution image (with red path)
        img_solution_b64 = render_graph_image(NODES, EDGES, path_nodes=SHORTEST_PATH,
                                               title=f"Shortest path from {SOURCE} to {TARGET}")
        img_solution_uri = f"data:image/png;base64,{img_solution_b64}"

        qn = question_number
        name_input_array.append([
            (f"nodeslist_question{qn}", f"nodes_question{qn}", nodes_str),
            (f"edgeslist_question{qn}", f"edges_question{qn}", edges_str),
            (f"sourcelist_question{qn}", f"source_question{qn}", SOURCE),
            (f"targetlist_question{qn}", f"target_question{qn}", TARGET),
            (f"shortestpathlist_question{qn}", f"shortestpath_question{qn}", path_str),
            (f"distancelist_question{qn}", f"distance_question{qn}", dist_str),
            # Only Data-URIs (no imgb64)
            (f"imgdataurilist_question{qn}", f"imgdatauri_question{qn}", img_question_uri),
            (f"imgsolutionlist_question{qn}", f"imgsolution_question{qn}", img_solution_uri),
        ])

        image_input_array.append((
            f"dijkstra_q{question_number}_i{inst_num+1}_question.png",
            img_question_b64,
            timestamp
        ))
        image_input_array.append((
            f"dijkstra_q{question_number}_i{inst_num+1}_solution.png",
            img_solution_b64,
            timestamp
        ))

    var_names = [(t[0], t[1]) for t in name_input_array[0]]

    final_triplets = []
    for idx, (list_name, single_name) in enumerate(var_names):
        values = [inst[idx][2] for inst in name_input_array]
        formatted_list = format_list_of_strings(values)
        final_triplets.append((list_name, single_name, formatted_list))

    return final_triplets, image_input_array, question_amount

if __name__ == "__main__":
    folder_path = r"C:\Users\omidf\OneDrive\Taxi\UAS\Semester 5\Projekt\V1"

    question_number = 7
    seed = None  # None = random each time; set to 123 for reproducible results
    num_instances = 3  # OPTIMIZED: 3 instances (was 10)

    clear_variable_declarations(folder_path)
    clear_resources(folder_path)

    name_input_array, image_input_array, question_amount = build_5node_instances(
        question_number=question_number,
        k=num_instances,
        seed=seed
    )

    format_to_xml(
        folder_path,
        name_input_array,
        question_number,
        question_amount
    )

    format_images_to_xml(folder_path, image_input_array)

    print(f"Generated {question_amount} 5-node Dijkstra tasks (optimized).")
