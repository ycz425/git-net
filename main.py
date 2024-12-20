import data.data_access as da
from src.render import render_graph
import src.graph as graph

if __name__ == '__main__':
    repos = da.get_repositories()
    forks = da.get_forks()
    users = da.get_users()
    stars = da.get_stars()
    nodes = [(repo['id'], {'type': 'repo'}) for repo in repos]
    nodes += [(user['id'], {'type': 'user'}) for user in users]
    edges = [(fork['id'], fork['parent_id']) for fork in forks if fork['parent_id'] is not None]
    edges += [(star['user_id'], star['repo_id']) for star in stars]
    G = graph.construct(nodes, edges)
    render_graph(G)