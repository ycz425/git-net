from dash import Dash, html, dcc, callback, Output, Input, State
from src.render import create_figure
import pickle
import plotly.graph_objects as go
from src.recommendation import recommend_repos
import src.graph as graph


with open('data/graphs/data.pkl', 'rb') as file:
    G = pickle.load(file)

create_figure(G)

app = Dash()
app.layout = [
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H1('GitNet', style={'font-size': '36px'}),
                    html.P('GitHub Graph Analysis and Recommendation', style={'font-size': '28px'}),
                ],
                style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'gap': '1.25rem', 'border-bottom': '1px solid white'}
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.P('User Visibility:', style={'font-weight': 'bold'}),
                            dcc.RadioItems(
                                id='user-visibility',
                                options=[{'label': 'Hide', 'value': False}, {'label': 'Show', 'value': True}],
                                value=False
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            html.P('Color Grouping:', style={'font-weight': 'bold'}),
                            dcc.RadioItems(
                                id='color-group',
                                options=[{'label': 'Communities', 'value': True}, {'label': 'Connected Components', 'value': False}],
                                value=False,
                            )
                        ]
                    ),
                    html.Div(
                        children=[
                            html.Button('Reset View', id='reset-button', n_clicks=0)
                        ]
                    )
                ],
                style={'display': 'flex', 'flex-direcition': 'row', 'align-items': 'end', 'gap': '2rem', 'border-bottom': '1px solid white', 'padding-bottom': '20px'}
            ),
        ],
        style={'padding-left': '40px', 'padding-right': '40px', 'padding-top': '5px'}
    ),
    dcc.Store(id='figure'),
    dcc.Store(id='click_data'),
    dcc.Store(id='prev_n_clicks'),
    dcc.Loading(
        id="loading-graph",
        type="circle",
        children=[
            dcc.Graph(
                id='graph',
                figure={},
                style={'height': '100vh', 'margin': '0', 'padding-left': '40px', 'padding-right': '40px'}
            )
        ],
    )
]


@callback(
    [
        Output(component_id='graph', component_property='figure'),
        Output(component_id='figure', component_property='data'),
        Output(component_id='graph', component_property='clickData'),
        Output(component_id='prev_n_clicks', component_property='data')
    ],
    [
        Input(component_id='user-visibility', component_property='value'),
        Input(component_id='color-group', component_property='value'),
        Input(component_id='graph', component_property='clickData'),
        Input(component_id='reset-button', component_property='n_clicks')
    ],
    [
        State(component_id='figure', component_property='data'),
        State(component_id='prev_n_clicks', component_property='data')
    ]
)
def update_graph(user_visible, show_communities, click_data, n_clicks, fig, prev_n_clicks):
    if fig is None or n_clicks != prev_n_clicks:
        fig = create_figure(G).to_dict()
        
    if user_visible and show_communities:
        fig['data'][1]['visible'] = True 
        fig['data'][2]['visible'] = False
        fig['data'][3]['visible'] = True
        fig['data'][4]['visible'] = False
        fig['data'][5]['visible'] = True
    elif user_visible and not show_communities:
        fig['data'][1]['visible'] = True 
        fig['data'][2]['visible'] = True
        fig['data'][3]['visible'] = False
        fig['data'][4]['visible'] = True
        fig['data'][5]['visible'] = False
    elif not user_visible and show_communities:
        fig['data'][1]['visible'] = False
        fig['data'][2]['visible'] = False
        fig['data'][3]['visible'] = False
        fig['data'][4]['visible'] = False
        fig['data'][5]['visible'] = True
    else:
        fig['data'][1]['visible'] = False
        fig['data'][2]['visible'] = False
        fig['data'][3]['visible'] = False
        fig['data'][4]['visible'] = True
        fig['data'][5]['visible'] = False
    
    if click_data  and 'customdata' in click_data['points'][0] and click_data['points'][0]['customdata']['id'].startswith('user'):
        results = set(recommend_repos(G, click_data['points'][0]['customdata']['id'], 10))
        for trace in fig['data']:
            if trace['name'] == 'nodes':
                for i in range(len(trace['x'])):
                    if trace['customdata'][i]['id'] in results:
                        trace['marker']['line']['width'][i] = 2
                        trace['marker']['opacity'][i] = 1
                    elif trace['customdata'][i]['id'] == click_data['points'][0]['customdata']['id']:
                        trace['marker']['line']['width'][i] == 10
                        trace['marker']['opacity'][i] = 1
                    else:
                        trace['marker']['line']['width'][i] = 0.5
                        trace['marker']['opacity'][i] = 0.15
            else:
                trace['line']['width'] = 0.1

    return fig, fig, None, n_clicks


if __name__ == '__main__':
    app.run(debug=True)
    