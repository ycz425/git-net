import data.data_access as da
from src.render import render_graph
import src.graph as graph
from src.recommendation import recommend_repos


if __name__ == '__main__':
    G = graph.construct(include_users=False)
    render_graph(G, show_communities=False)