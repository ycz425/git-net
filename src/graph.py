import networkx as nx
from collections import deque
from data.scripts import data_access as da
import pickle


def construct(include_users=False, spring_layout_iterations=50, save=False) -> nx.Graph:
    repos = da.get_repositories()
    forks = da.get_forks()
    users = da.get_users()
    stars = da.get_stars()

    nodes = []
    edges = []

    if include_users:
        nodes += [(user['id'], {'type': 'user', 'login': user['login']}) for user in users]
        edges += [(star['user_id'], star['repo_id']) for star in stars]

    nodes += [(repo['id'], {'type': 'repo', 'full_name': repo['full_name']}) for repo in repos]
    edges += [(fork['id'], fork['parent_id']) for fork in forks if fork['parent_id'] is not None]

    G = nx.Graph() 
    G.add_nodes_from(nodes) 
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, iterations=spring_layout_iterations)
    nx.set_node_attributes(G, pos, 'pos')

    if save:
        with open('data/graphs/repos_and_users.pkl' if include_users else 'data/graphs/repos.pkl', 'wb') as file:
            pickle.dump(G, file)
            
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
    

def max_degree_repo(G: nx.Graph) -> tuple[str, int]:
    return max([deg_view for deg_view in G.degree if G.nodes[deg_view[0]]['type'] == 'repo'], key=lambda x: x[1])


def max_degree_user(G: nx.Graph) -> tuple[str, int]:
    return max([deg_view for deg_view in G.degree if G.nodes[deg_view[0]]['type'] == 'user'], key=lambda x: x[1])


def single_source_shortest_paths(G: nx.Graph, source: str) -> tuple[dict, dict, dict]:
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


def betweenness_centrality(G: nx.Graph) -> dict[str, float]:
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
                        

        


                    
