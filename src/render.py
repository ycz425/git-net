import pickle
import networkx as nx
import distinctipy
import matplotlib.colors as mcolors
import plotly.graph_objects as go
from networkx.algorithms.community import louvain_communities
import src.graph as graph


def _create_node_trace(G: nx.Graph, type: str) -> go.Scatter:
    node_x = []
    node_y = []
    nodes = []
    for node in G.nodes():
        if G.nodes[node]['type'] == type:
            x, y = G.nodes[node]['pos']
            nodes.append(node)
            node_x.append(x)
            node_y.append(y)


    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=[f'Repo: {G.nodes[node]['full_name']}' if G.nodes[node]['type'] == 'repo' else f'User: {G.nodes[node]['login']}' for node in nodes],
        marker=dict(
            size=10,
            color=[G.nodes[node]['color'] for node in nodes],
            line=dict(
                color='white',
                width=1
            )
        )
    )

    return node_trace


def _create_edge_trace(G: nx.Graph, type: str) -> go.Scatter:
    edge_x = []
    edge_y = []
    for edge in G.edges():
        if (
            (type == 'fork' and edge[0].startswith('repo') and edge[1].startswith('repo')) or
            (type == 'star' and (edge[0].startswith('user') or edge[1].startswith('user')))
        ):
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        hoverinfo='none',
        line=dict(width=0.5, color='#ffffff')
    )

    return edge_trace



def create_figure(show_communities=False) -> go.Figure:
    with open('data/graphs/repos_and_users.pkl', 'rb') as file:
        G = pickle.load(file)

    groups = louvain_communities(G) if show_communities else [set(g) for g in graph.connected_repos(G)]
    group_colors = [mcolors.to_hex(color) for color in distinctipy.get_colors(len(groups))]
    for node in G.nodes():
        if not show_communities and G.nodes[node]['type'] == 'user':
            G.nodes[node]['color'] = '#E0E0E0'
        else:
            for i, group in enumerate(groups):
                if node in group:
                    G.nodes[node]['color'] = group_colors[i]
                    break

    repo_node_trace = _create_node_trace(G, 'repo')
    user_node_trace = _create_node_trace(G, 'user')
    fork_edge_trace = _create_edge_trace(G, 'fork')
    star_edge_trace = _create_edge_trace(G, 'star')

    fig = go.Figure(
        data=[fork_edge_trace, star_edge_trace, user_node_trace, repo_node_trace],
        layout=go.Layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0,l=0,r=0,t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )
    return fig
