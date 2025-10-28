import random

# Nodes
nodes = ["Berlin", "Paris", "London", "Prague", "Vienna"]

# Edges (tuples: node1, node2, weight)
def generate_edges():
    edges = [
        ("Berlin", "Paris", random.randint(1, 10)),
        ("Berlin", "Prague", random.randint(1, 10)),
        ("Paris", "London", random.randint(1, 10)),
        ("Paris", "Vienna", random.randint(1, 10)),
        ("London", "Prague", random.randint(1, 10)),
        ("Prague", "Vienna", random.randint(1, 10)),
    ]
    return edges
