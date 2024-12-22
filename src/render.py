import networkx as nx
import distinctipy
import matplotlib.colors as mcolors
import plotly.graph_objects as go
from networkx.algorithms.community import louvain_communities
import src.graph as graph

def render_graph(G: nx.Graph, show_communities=False, layout_file=None) -> None:
    groups = louvain_communities(G) if show_communities else [set(g) for g in graph.connected_repos(G)]
    group_colors = [mcolors.to_hex(color) for color in distinctipy.get_colors(len(groups))]
    for i in range(len(groups)):
        g = groups[i]
        for node in g:
            G.nodes[node]['group'] = i

    pos = nx.spring_layout(G, iterations=100)
    nx.set_node_attributes(G, pos, 'pos')

    edge_x = []
    edge_y = []
    for edge in G.edges():
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

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=[f'Repo: {G.nodes[node]['full_name']}' if G.nodes[node]['type'] == 'repo' else f'User: {G.nodes[node]['login']}' for node in G.nodes()],
        marker=dict(
            size=10,
            color=['#E0E0E0' if not show_communities and G.nodes[node]['type'] == 'user' else group_colors[G.nodes[node]['group']] for node in G.nodes()],
            line=dict(
                color='white',
                width=1
            )
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text="GitNet",
                font=dict(
                    size=30,
                    weight="bold" 
                ),
                y=0.95,                  
                yanchor='top',  
            ),
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig.show()
