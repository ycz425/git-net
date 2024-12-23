from dash import Dash, html, dcc, callback, Output, Input
from src.render import create_figure

app = Dash()
app.layout =[
    html.H1('GitNet'),
    html.H2('GitHub Graph Analysis and Recommendation'),
    dcc.RadioItems(
        id='user-visibility',
        options=[{'label': 'Hide users', 'value': False}, {'label': 'Show users', 'value': True}],
        value=False
    ),
    dcc.Graph(
        id='graph',
        figure={},
        style={'height': '100vh', 'width': '100vw', 'margin': '0'}
    )
]
fig = create_figure(show_communities=False)

@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='user-visibility', component_property='value')
)
def update_graph(user_visible):
    if user_visible:
        fig.data[1].visible = True
        fig.data[2].visible = True
    else:
        fig.data[1].visible = False
        fig.data[2].visible = False

    return fig




if __name__ == '__main__':
    app.run(debug=True)
    