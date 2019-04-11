import deliveries as py
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE],
                meta_tags=[{'name': 'viewport', 'content': "width=device-width, initial-scale=1"}])
app.title = "IPL Analytics"

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
    'Wickets by over': py.wickets_by_over,
    'No. of wickets by player': py.most_wickets_against
}

vs_types_of_graph = {
    'Strike rate': py.strike_rate_batsman_bowler,
    'Distribution of wickets': py.wickets_batsman_bowler
}

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("GitHub", href="https://www.github.com/lakshyaag", active=True)),
        dbc.NavItem(dbc.NavLink("Made by Lakshya Agarwal", href="#")),
    ],
    brand='IPL Analytics',
    brand_href='https://ipldash.herokuapp.com',
    color='primary',
    dark=True,
    fluid=True,
)

header = dbc.Row([
    dbc.Col([
        html.H2('Indian Premier League'),
        html.P('''
        The Indian Premier League is a professional Twenty20 cricket league in India contested during March or April and 
        May of every year by eight teams representing eight different cities in India.
        '''),

        html.Div(
            [
                dbc.Button("Teams playing", id='teams-playing', className='mb-2'),
                dbc.Collapse(
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem('Chennai Super Kings'),
                            dbc.ListGroupItem('Mumbai Indians'),
                            dbc.ListGroupItem('Kolkata Knight Riders'),
                            dbc.ListGroupItem('Royal Challengers Bangalore'),
                            dbc.ListGroupItem('Kings XI Punjab'),
                            dbc.ListGroupItem('Sunrisers Hyderabad'),
                            dbc.ListGroupItem('Rajasthan Royals'),
                            dbc.ListGroupItem('Delhi Capitals'),
                        ]
                    ),
                    id='collapse'
                )
            ]
        )
    ], width=6),
    dbc.Col([
        html.H2('Analytics Dashboard'),
        html.P('''
        An interactive analytics dashboard for IPL which contains data from all seasons till 2018. 
        '''),
        html.P('''
        You can analyze runs scored, dismissals, strike rates by player, toss statistics and other insights.''')
    ], width=6),
], className='mt-4')

batsman_section = dbc.Card(
    dbc.CardBody([
        html.Label(
            "Graph",
            htmlFor='graph_type_bat'
        ),
        dcc.Dropdown(
            id='graph_type_bat',
            options=[{'label': i, 'value': i} for i in batsman_types_of_graph.keys()],
            placeholder='Select graph',
            value="Runs per season"
        ),

        html.Label(
            "Batsman",
            htmlFor='batsman_name'
        ),

        dcc.Dropdown(
            id='batsman_name',
            options=[{'label': x, 'value': x} for x in batsman_names],
            placeholder='Select batsman',
            value='RG Sharma'
        ),

        dcc.Graph(
            id='graph_bat',
            className='graph_fill'
        ),
    ])
)

bowler_section = dbc.Card(
    dbc.CardBody([
        html.Label(
            "Graph",
            htmlFor='graph_type_bowl'
        ),
        dcc.Dropdown(
            id='graph_type_bowl',
            options=[{'label': i, 'value': i} for i in bowler_types_of_graph.keys()],
            value='Runs conceded per season',
            placeholder='Select graph'
        ),
        html.Label(
            "Bowler",
            htmlFor='bowler_name'
        ),
        dcc.Dropdown(
            id='bowler_name',
            options=[{'label': x, 'value': x} for x in bowler_names],
            value='B Kumar',
            placeholder='Select bowler'
        ),

        dcc.Graph(
            id='graph_bowl',
            className='graph_fill',
            config={
                'showTips': True
            }
        ),
    ])
)

player_v_player_section = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Label(
                    "Graph",
                    htmlFor='graph_vs_type'
                ),
                dcc.Dropdown(
                    id='graph_vs_type',
                    options=[{'label': i, 'value': i} for i in vs_types_of_graph.keys()],
                    value='Strike rate',
                    placeholder='Select type of graph'
                ),
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Label(
                    'Batsman',
                    htmlFor='batsman_vs'
                ),
                dcc.Dropdown(
                    id='batsman_vs',
                    options=[{'label': i, 'value': i} for i in batsman_names],
                    value='RG Sharma',
                    placeholder='Select batsman',
                ),
            ], width=6),
            dbc.Col([
                html.Label(
                    'Bowler',
                    htmlFor='bowler_vs'
                ),
                dcc.Dropdown(
                    id='bowler_vs',
                    options=[{'label': i, 'value': i} for i in bowler_names],
                    value='B Kumar',
                    placeholder='Select bowler'
                ),
            ], width=6),
        ]),

        dcc.Graph(
            id='batsman_v_bowler',
            className='graph_fill'
        )
    ])
])

toss_section = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Span(children=[
                    html.H5('Toss Outcome'),
                    dbc.RadioItems(
                        id='toss_cond',
                        options=[
                            {'label': "Win", "value": 'win'},
                            {'label': "Lose", "value": 'lose'}
                        ],
                        value='win',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center'}),
            ], width=6),

            dbc.Col(children=[
                html.Span(children=[
                    html.H5('Toss Decision'),
                    dbc.RadioItems(
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
                    id='toss_graph',
                    className='graph_fill'
                )
            ])
        ])
    ])
])

tabs = dbc.Tabs(
    [
        dbc.Tab(batsman_section, label="Batsman", tab_id='batsman_tab', labelClassName='text-dark'),
        dbc.Tab(bowler_section, label="Bowler", tab_id='bowler_tab', labelClassName='text-dark'),
        dbc.Tab(player_v_player_section, label='Player vs. Player', tab_id='player_v_player_tab',
                labelClassName='text-dark'),
        dbc.Tab(toss_section, label='Toss Analysis', tab_id='toss_tab', labelClassName='text-dark')
    ],
    active_tab='batsman_tab',
    id='tabs')

body = dbc.Container(fluid=True, children=[
    header,
    dbc.Row([
        dbc.Col([
            tabs
        ])
    ], className='mt-4'),
])

app.layout = html.Div(children=[navbar, body])


@app.callback(
    Output(component_id='graph_bat', component_property='figure'),
    [Input(component_id='graph_type_bat', component_property='value'),
     Input(component_id='batsman_name', component_property='value'),
     Input('tabs', 'active_tab')]
)
def update_batsman_graph(type_graph, name, t):
    return batsman_types_of_graph[type_graph](name)


@app.callback(
    Output(component_id='graph_bowl', component_property='figure'),
    [Input(component_id='graph_type_bowl', component_property='value'),
     Input(component_id='bowler_name', component_property='value'),
     Input('tabs', 'active_tab')]
)
def update_bowler_graph(type_graph, name, t):
    return bowler_types_of_graph[type_graph](name)


@app.callback(
    Output(component_id='batsman_v_bowler', component_property='figure'),
    [Input(component_id='graph_vs_type', component_property='value'),
     Input(component_id='batsman_vs', component_property='value'),
     Input(component_id='bowler_vs', component_property='value'),
     Input('tabs', 'active_tab')]
)
def batsman_v_bowler_graph(type_graph, batsman_name, bowler_name, t):
    return vs_types_of_graph[type_graph](batsman_name, bowler_name)


@app.callback(
    Output(component_id='toss_graph', component_property='figure'),
    [Input(component_id='toss_cond', component_property='value'),
     Input(component_id='toss_decision', component_property='value'),
     Input('tabs', 'active_tab')]
)
def update_toss_graph(toss_cond, toss_decision, t):
    return py.outcome_by_toss(toss_cond, toss_decision)


@app.callback(
    Output('collapse', 'is_open'),
    [Input('teams-playing', 'n_clicks')],
    [State('collapse', 'is_open')]
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
