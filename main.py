import data.data_access as da
from src.render import render_graph
import src.graph as graph

if __name__ == '__main__':
    repos = da.get_repositories()
    forks = da.get_forks()
    nodes = [(repo['id'], {'name': repo['full_name'], 'stars': repo['stargazers_count']}) for repo in repos]
    edges = [(fork['id'], fork['parent_id']) for fork in forks if fork['parent_id'] is not None]
    G = graph.construct(nodes, edges)
    render_graph(G)