from dash import Dash, html, dcc, callback, Output, Input, State
from src.render import create_figure
import pickle
import plotly.graph_objects as go


with open('data/graphs/repos_and_users.pkl', 'rb') as file:
    G = pickle.load(file)

create_figure(G)

app = Dash()
app.layout =[
    html.H1('GitNet'),
    html.H2('GitHub Graph Analysis and Recommendation'),
    dcc.Store(id='figure'),
    dcc.RadioItems(
        id='user-visibility',
        options=[{'label': 'Hide users', 'value': False}, {'label': 'Show users', 'value': True}],
        value=False
    ),
    dcc.RadioItems(
        id='color-group',
        options=[{'label': 'Show communities', 'value': True}, {'label': 'Show connected components', 'value': False}],
        value=False
    ),
    dcc.Loading(
        id="loading-graph",
        type="circle",
        children=[
            dcc.Graph(
                id='graph',
                figure={},
                style={'height': '100vh', 'width': '100vw', 'margin': '0'}
            )
        ],
    )
]


@callback(
    [
        Output(component_id='graph', component_property='figure'),
        Output(component_id='figure', component_property='data')
    ],
    [
        Input(component_id='user-visibility', component_property='value'),
        Input(component_id='color-group', component_property='value')
    ],
    State(component_id='figure', component_property='data')
)
def update_user_visibility(user_visible, show_communities, fig):
    if fig is None:
        fig = create_figure(G)
    else:
        fig = go.Figure(fig)

    if user_visible and show_communities:
        fig.data[1].visible = True 
        fig.data[2].visible = False
        fig.data[3].visible = True
        fig.data[4].visible = False
        fig.data[5].visible = True
    elif user_visible and not show_communities:
        fig.data[1].visible = True 
        fig.data[2].visible = True
        fig.data[3].visible = False
        fig.data[4].visible = True
        fig.data[5].visible = False
    elif not user_visible and show_communities:
        fig.data[1].visible = False
        fig.data[2].visible = False
        fig.data[3].visible = False
        fig.data[4].visible = False
        fig.data[5].visible = True
    else:
        fig.data[1].visible = False
        fig.data[2].visible = False
        fig.data[3].visible = False
        fig.data[4].visible = True
        fig.data[5].visible = False

    return fig, fig.to_dict()


if __name__ == '__main__':
    app.run(debug=True)
    