import networkx as nx

def construct(nodes: list, edges: list) -> nx.Graph:
    G = nx.Graph() 
    G.add_nodes_from(nodes) 
    G.add_edges_from(edges)

    return G


def connected_repos(G: nx.Graph) -> list[nx.Graph]:
    """ Connected component analysis
    """
    visited = set()
    result = []

    for node in G.nodes():
        if G.nodes[node]['type'] == 'repo' and node not in visited:
            sub_G = nx.Graph()
            stack = [node]

            while len(stack) > 0:
                curr = stack.pop()
                visited.add(curr)
                sub_G.add_nodes_from([(curr, G.nodes[curr])])
                
                for neighbor in G.neighbors(curr):
                    if G.nodes[neighbor]['type'] == 'repo':
                        sub_G.add_edges_from([(curr, neighbor)])
                        if neighbor not in visited:
                            stack.append(neighbor)

            result.append(sub_G)

    return result
            