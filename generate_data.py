import sys
import math
import json
import random

# Constants
MIN_VERTICES = 5
MAX_VERTICES = 100
NUM_HYPERGRAPHS = 100
data_file = "data/generated_hypergraphs.json"


def main():
    if len(sys.argv) != 2:
        print("Usage : python3 generate_data.py <no of vertices in hypergraph>")
        exit(0)
    n = int(sys.argv[1])
    if n < MIN_VERTICES or n > MAX_VERTICES:
        print("Invalid value for no. of vertices")
        exit(0)
    create_hypergraph_data(n)


def create_hypergraph_data(n):
    data = []
    for i in range(NUM_HYPERGRAPHS):
        h = {
            "label": i,
            "n": n,
            "edges": make_edges(n)
        }
        data.append(h)
    with open(data_file, 'w') as f:
        f.write(json.dumps(data))


def make_edges(n):
    edges = []
    num_edges = random.randint(n, n*n)
    for i in range(num_edges):
        e = [x for x in range(n)]
        random.shuffle(e)
        path_len = random.randint(int(math.sqrt(n)), 2*int(math.sqrt(n)))
        edges.append(e[:path_len])
    return edges


if __name__ == '__main__':
    main()
