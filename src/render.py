import networkx as nx
import distinctipy
import matplotlib.colors as mcolors
import plotly.graph_objects as go
from networkx.algorithms.community import louvain_communities
import src.graph as graph


def _get_group_color(node: str, groups: list[set], group_colors: list[str]):
    for i, group in enumerate(groups):
        if node in group:
            return group_colors[i]
    
    return '#E0E0E0'


def _create_node_trace(G: nx.Graph, type: str, groups: list[set]) -> go.Scatter:
    node_x = []
    node_y = []
    nodes = []
    for node in G.nodes():
        if G.nodes[node]['type'] == type:
            x, y = G.nodes[node]['pos']
            nodes.append(node)
            node_x.append(x)
            node_y.append(y)

    group_colors = [mcolors.to_hex(color) for color in distinctipy.get_colors(len(groups))]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        name='nodes',
        mode='markers',
        hoverinfo='text',
        text=[f'Repo: {G.nodes[node]['full_name']}' if G.nodes[node]['type'] == 'repo' else f'User: {G.nodes[node]['login']}' for node in nodes],
        customdata=[{'id': node} for node in nodes],
        marker=dict(
            size=10,
            color=[_get_group_color(node, groups, group_colors) for node in nodes],
            line=dict(
                color='white',
                width=[0.5] * len(nodes)
            ),
            opacity=[1] * len(nodes)
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
        name='edges',
        mode='lines',
        hoverinfo='none',
        line=dict(width=0.5, color='#aaaaaa')
    )

    return edge_trace



def create_figure(G: nx.Graph) -> go.Figure:
    communities = louvain_communities(G)
    connected_components = [set(g) for g in graph.connected_repos(G)]
    
    repo_node_component_trace = _create_node_trace(G, 'repo', connected_components)
    repo_node_community_trace = _create_node_trace(G, 'repo', communities)
    user_node_component_trace = _create_node_trace(G, 'user', connected_components)
    user_node_community_trace = _create_node_trace(G, 'user', communities)
    
    repo_node_community_trace.visible = False
    user_node_community_trace.visible = False

    fork_edge_trace = _create_edge_trace(G, 'fork')
    star_edge_trace = _create_edge_trace(G, 'star')

    fig = go.Figure(
        data=[
            fork_edge_trace,
            star_edge_trace,
            user_node_component_trace,
            user_node_community_trace,
            repo_node_component_trace,
            repo_node_community_trace
        ],
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

    