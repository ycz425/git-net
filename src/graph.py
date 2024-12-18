import networkx as nx

def construct(nodes: list, edges: list) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(nodes) 
    G.add_edges_from(edges)

    return G
