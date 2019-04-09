import deliveries as py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

server = app.server

batsman_names = py.balls.batsman.sort_values().unique()
bowler_names = py.balls.bowler.sort_values().unique()

batsman_types_of_graph = {
    'Runs per season': py.plot_batsman_runs,
    'Distribution of runs': py.distribution_of_runs,
    'Favorite venues': py.fav_venues,
    'Favorite bowlers': py.fav_bowlers,
    'Runs against teams': py.most_runs_against_team,
    'Runs by over': py.runs_by_over,
}

bowler_types_of_graph = {
    'Runs conceded per season': py.plot_bowler_runs,
    'Economy rate by season': py.plot_economy_rate,
    'Wickets by season': py.wicket_data,
    'Wickets by over': py.wickets_by_over
}

body = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col([
            html.H3(children='Dashboard of IPL Analytics', style={
                'textAlign': 'center'}),
        ])
    ]),

    dbc.Row([
        dbc.Col(children=[
            html.Div([
                html.H5(children='Batsman Section', style={
                    'textAlign': 'left'
                }),

                dcc.Dropdown(
                    id='graph_type_bat',
                    options=[{'label': i, 'value': i} for i in batsman_types_of_graph.keys()],
                    placeholder='Select graph',
                    value="Runs per season"
                ),

                dcc.Dropdown(
                    id='batsman_name',
                    options=[{'label': x, 'value': x} for x in batsman_names],
                    placeholder='Select batsman',
                    value='RG Sharma'
                ),

                dcc.Graph(
                    id='graph_bat',
                ),
            ]),
        ], width=6),

        dbc.Col(children=[
            html.Div([
                html.H5('Bowler section'),

                html.Div(children=[
                    dcc.Dropdown(
                        id='graph_type_bowl',
                        options=[{'label': i, 'value': i} for i in bowler_types_of_graph.keys()],
                        value='Runs conceded per season',
                        placeholder='Select graph'
                    ),

                    dcc.Dropdown(
                        id='bowler_name',
                        options=[{'label': x, 'value': x} for x in bowler_names],
                        value='B Kumar',
                        placeholder='Select bowler'
                    ),
                ]),

                dcc.Graph(
                    id='graph_bowl',
                ),
            ])
        ], width=6),
    ]),

    dbc.Row(children=[
        dbc.Col(children=[
            dcc.Graph(
                id='batsman_v_bowler',
            )
        ])
    ]),

    dbc.Row(children=[
        dbc.Col(children=[
            html.H4('Outcomes based on Toss'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Span(children=[
                html.H6('Toss Outcome'),
                dcc.RadioItems(
                    id='toss_cond',
                    options=[
                        {'label': "Win", "value": 'win'},
                        {'label': "Lose", "value": 'lose'}
                    ],
                    value='win',
                )
            ], style={'textAlign': 'center'}),
        ], width=6),

        dbc.Col(children=[
            html.Span(children=[
                html.H6('Toss Decision'),
                dcc.RadioItems(
                    id='toss_decision',
                    options=[
                        {'label': "Bat", "value": 'bat'},
                        {'label': "Field", "value": 'field'}
                    ],
                    value='bat',
                )
            ], style={'textAlign': 'center'}),
        ], width=6),
    ]),

    dbc.Row(children=[
        dbc.Col([
            dcc.Graph(
                id='toss_graph'
            )
        ])
    ])
])

app.layout = html.Div(children=[body])


@app.callback(
    Output(component_id='graph_bat', component_property='figure'),
    [Input(component_id='graph_type_bat', component_property='value'),
     Input(component_id='batsman_name', component_property='value')]
)
def update_graph(type_graph="Runs per season", name=""):
    return batsman_types_of_graph[type_graph](name)


@app.callback(
    Output(component_id='batsman_v_bowler', component_property='figure'),
    [Input(component_id='batsman_name', component_property='value'),
     Input(component_id='bowler_name', component_property='value')]
)
def batsman_v_bowler_graph(batsman_name, bowler_name):
    return py.batsman_v_bowler(batsman_name, bowler_name)


@app.callback(
    Output(component_id='graph_bowl', component_property='figure'),
    [Input(component_id='graph_type_bowl', component_property='value'),
     Input(component_id='bowler_name', component_property='value')]
)
def update_graph(type_graph="Runs per season", name=""):
    return bowler_types_of_graph[type_graph](name)


@app.callback(
    Output(component_id='toss_graph', component_property='figure'),
    [Input(component_id='toss_cond', component_property='value'),
     Input(component_id='toss_decision', component_property='value')]
)
def update_toss_graph(toss_cond, toss_decision):
    return py.outcome_by_toss(toss_cond, toss_decision)


if __name__ == '__main__':
    app.run_server(debug=True)
