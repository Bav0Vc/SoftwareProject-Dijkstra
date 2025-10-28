"""
This is ONLY an example, provided for illustrative purposes and to inspire your own ideas!!!
Keep an eye on the standards. These were not taken into account here!

Generate N (default 3) Graph tasks (A->B->C) for JACK3 with dynamic images.

- Graph: A->B, B->C, A->C with random integer weights
- Constraint: w(A,B) + w(B,C) < w(A,C) so the cheapest A->C path is A->B->C
- Writes variables and images to your Exercise XML
- Exposes both Base64 and ready-to-use Data-URI per instance:
    imgb64_question_<n>, imgdatauri_question_<n>

In JACK3 task text, embed the correct image dynamically via:
    <img style="max-width:100%;" src="[var=imgdatauri_question_7]" />

Requirements:
- pip install graphviz Pillow
- Helper modules in the same folder:
  - append_question_number_to_string.py
  - formatter_for_copy_paste_export_to_jack3.py
  - formatter_to_xml.py
  - dijkstra 3610096.xml (as example Exercise XML to write to)
"""

from datetime import datetime
import random
import base64
import graphviz as gv

# Helper modules (existing files in your project)
from append_question_number_to_string import append_question_number_to_string
from formatter_for_copy_paste_export_to_jack3 import format_list_of_strings, format_list_of_values
from formatter_to_xml import format_to_xml, clear_variable_declarations, format_images_to_xml, clear_resources

# Render a single ABC graph image
def render_graph_image(nodes, edges, path_nodes, title):
    dot = gv.Digraph("abc_dijkstra")
    dot.attr("graph", dpi="150", rankdir="LR", label=title, labelloc="t")
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

# Random weights with enforced constraint ab+bc < ac (Just an example!)
def random_abc_weights(wmin=1, wmax=9, rng=None):
    r = rng or random
    while True:
        ab = r.randint(wmin, wmax)
        bc = r.randint(wmin, wmax)
        # ensure AC strictly larger than AB+BC! (Just an example!)
        ac_low = max(ab + bc + 1, wmin + 1)
        ac_high = max(ac_low, wmax * 2)
        ac = r.randint(ac_low, ac_high)
        if ab + bc < ac:
            return ab, bc, ac

# Build variables & images for k instances
def build_abc_instances(question_number: int, k: int = 3, seed: int | None = 123):
    rng = random.Random(seed)

    nodes_all = []        # ["A,B,C", ...]
    edges_all = []        # ["A,B,2;B,C,3;A,C,8", ...]
    sources_all = []      # ["A", ...]
    targets_all = []      # ["C", ...]
    dists_all = []        # [ab+bc, ...]
    paths_all = []        # ["A,B,C", ...]
    imgb64_all = []       # pure base64 per instance
    imgdatauri_all = []   # 'data:image/png;base64,<b64>' per instance
    images = []           # resources: (filename, base64, iso_timestamp)

    NODES = ["A", "B", "C"]
    SOURCE, TARGET = "A", "C"
    SHORTEST_PATH = ["A", "B", "C"]

    for i in range(k):
        ab, bc, ac = random_abc_weights(rng=rng)
        EDGES = [("A", "B", ab), ("B", "C", bc), ("A", "C", ac)]
        best_cost = ab + bc

        # strings for JACK3 lists
        nodes_all.append("A,B,C")
        edges_all.append(";".join([f"{u},{v},{w}" for (u, v, w) in EDGES]))
        sources_all.append(SOURCE)
        targets_all.append(TARGET)
        dists_all.append(best_cost)
        paths_all.append(",".join(SHORTEST_PATH))

        # image (both as resource and as variables)
        img_b64 = render_graph_image(
            NODES, EDGES, SHORTEST_PATH,
            title=f"Dijkstra – shortest path from {SOURCE} to {TARGET}"
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
    # Set the folder that contains exactly ONE Exercise XML (e.g., test.xml)
    folder_path = r"path_to_your_resources"   # <-- adjust
    question_number = 7
    seed = 123
    num_instances = 3

    # Clear previous variables/resources
    clear_variable_declarations(folder_path)
    clear_resources(folder_path)

    # Build variables + images
    name_input_array, image_input_array, question_amount = build_abc_instances(
        question_number=question_number,
        k=num_instances,
        seed=seed
    )

    # Write variables (includes imgb64s/imgb64 and imgdatauris/imgdatauri)
    format_to_xml(folder_path, name_input_array, question_number, question_amount)

    # Also add images as ExerciseResources
    format_images_to_xml(folder_path, image_input_array)

    print(f"Generated {question_amount} A→B→C Dijkstra tasks with dynamic images.")
