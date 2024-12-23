import data.scripts.data_access as da
from src.render import render_graph
import src.graph as graph
from src.recommendation import recommend_repos


if __name__ == '__main__':
    render_graph(include_users=True, show_communities=True)
    