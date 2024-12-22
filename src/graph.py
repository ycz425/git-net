import networkx as nx
from collections import deque

def construct(nodes: list, edges: list) -> nx.Graph:
    G = nx.Graph() 
    G.add_nodes_from(nodes) 
    G.add_edges_from(edges)

    return G


def connected_repos(G: nx.Graph) -> list[nx.Graph]:
    visited = set()
    result = []

    for node in G.nodes():
        if G.nodes[node]['type'] == 'repo' and node not in visited:
            sub_G = nx.Graph()
            stack = [node]
            visited.add(node)
            while len(stack) > 0:
                curr = stack.pop()
                sub_G.add_nodes_from([(curr, G.nodes[curr])])
                
                for neighbor in G.neighbors(curr):
                    if G.nodes[neighbor]['type'] == 'repo' and neighbor not in visited:
                        sub_G.add_edges_from([(curr, neighbor)])
                        visited.add(neighbor)
                        stack.append(neighbor)

            result.append(sub_G)

    return result
    

def max_degree_repo(G: nx.Graph) -> tuple[int, int]:
    return max([deg_view for deg_view in G.degree if G.nodes[deg_view[0]]['type'] == 'repo'], key=lambda x: x[1])


def max_degree_user(G: nx.Graph) -> tuple[int, int]:
    return max([deg_view for deg_view in G.degree if G.nodes[deg_view[0]]['type'] == 'user'], key=lambda x: x[1])


def single_source_shortest_paths(G: nx.Graph, source: int) -> tuple[dict, dict, dict]:
    queue = deque([source])
    dist = {node: -1 for node in G.nodes()}
    pred = {node: [] for node in G.nodes()}
    sigma = {node: 0 for node in G.nodes()}

    dist[source] = 0
    sigma[source] = 1

    while len(queue) > 0:
        curr = queue.popleft()

        for neighbor in G.neighbors(curr):
            if dist[neighbor] == -1:
                dist[neighbor] = dist[curr] + 1
                queue.append(neighbor)

            if dist[neighbor] == dist[curr] + 1:
                pred[neighbor].append(curr)
                sigma[neighbor] += sigma[curr]

    return dist, pred, sigma


def betweenness_centrality(G: nx.Graph) -> dict[int, float]:
    betweenness = {node: 0 for node in G.nodes()}
    for s in G.nodes():
        dist, pred, sigma = single_source_shortest_paths(G, s)
        delta = {node: 0 for node in G.nodes()}
        stack = sorted(dist.keys(), key=lambda x: dist[x], reverse=True)
        for t in stack:
            for v in pred[t]:
                delta[v] += sigma[v] / sigma[t] * (1 + delta[t])
            if t != s:
                betweenness[t] += delta[t]

    n = len(G.nodes())
    for node in betweenness:
        betweenness[node] /= (n - 1) * (n - 2)

    return betweenness
                        

        


                    
