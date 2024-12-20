import networkx as nx
from src.graph import connected_components
import distinctipy
import matplotlib.colors as mcolors
import plotly.graph_objects as go

def render_graph(G: nx.Graph) -> None:
    components = connected_components(G)
    for i in range(len(components)):
        g = components[i]
        for node in g.nodes():
            G.nodes[node]['group'] = i

    GROUP_COLORS = [mcolors.to_hex(color) for color in distinctipy.get_colors(20)]

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
        line=dict(width=0.5, color='#888')
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
        marker=dict(
            size=10,
            color=['red' if G.nodes[node]['type'] == 'repo' else GROUP_COLORS[G.nodes[node]['group']] for node in G.nodes()]
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text="<br>Network graph made with Python",
                font=dict(
                    size=16
                )
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig.show()
