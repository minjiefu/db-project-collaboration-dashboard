
from dash import Dash, html, dcc, Input, Output, dash_table, callback, State, ctx, no_update
from mongodb_utils import get_top_10_keywords
from mysql_utils import get_keywords, get_trends, get_potential_research_keywords, add_potential_keyword, get_top10_faculty_related_favorite_keywords, delete_potential_keyword, get_faculty_info, queryFaculties, get_notes, add_to_notes, delete_from_notes
from neo4j_utils import getConnectionsToFaculty
import pandas as pd
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import plotly.express as px

# create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container([
    ### Title Row ###
    dbc.Row([
        html.H1("Roadmap of Seeking Research Collaborators", style={'color': 'DarkRed', 'textAlign': 'center'}),
    ], align="center", justify = "center", className='pt-3'),

    ### Row 1 ###
    dbc.Row([
        ### Widget 1 ###
        dbc.Col([
            html.H1('Top 10 most popular research keywords', style={'color': 'FireBrick', 'textAlign': 'center'}),
            dbc.Row([
                dcc.RangeSlider(
                    id='year-slider',
                    min=1980,
                    max=2025,
                    value=[1980, 2025],
                    marks={str(year): str(year)
                           for year in range(1980, 2026, 5)},
                    tooltip={"placement": "top", "always_visible": True}
                )
            ], class_name='my-3'),
            
            dbc.Row([
                dcc.Graph(id = "keyword-bar", figure = {})
            ], class_name='my-3')
        ], width=5),
        ### Widget 2 ###
        dbc.Col([ 
            html.H1("Trends of keywords", style={'color': 'FireBrick', 'textAlign': 'center'}),
            dbc.Row([
                dcc.Dropdown(get_keywords(), 'data mining', id='dropdown-selection', style={'font-family': 'Georgia'})
            ], class_name='pt-4'),
            dbc.Row([
                dcc.Graph(id='graph-content', figure = {})
            ], class_name='my-3')
        ], width=5)
    ], class_name='p-3 d-flex justify-content-around'),

    ### Row 2 ###
    dbc.Row([
        ### Widget 3 ###
        dbc.Col([
            html.H1("Define Potential Research Interests", style={'color': 'FireBrick', 'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(get_keywords(), "", id='keyword-dropdown')
                ]),
                dbc.Col([
                    dbc.Button('Add', id='add-potential-keyword-button', n_clicks=0, color='secondary', className='mr-2')
                ]),
            ], className='my-3'),
            dbc.Row([
                dash_table.DataTable(
                    id='potential-keywords-table',
                    columns=[{"name": "Potential Research Interests", "id": "Potential Research Keywords"}],
                    data= [{"Potential Research Keywords": k} for k in get_potential_research_keywords()],
                    sort_action="native",
                    sort_mode="multi",
                    row_deletable=True,
                    page_size=10,
                    style_cell={'textAlign': 'left', 'font-family': 'Georgia'},
                    style_header={
                        'backgroundColor': 'FireBrick', 'color': 'white', 'textAlign': 'center', 'font-family': 'Georgia'},
                ),
            ], className='my-3')
        ], width=3),
        ### Widget 4 ###
        dbc.Col([
            html.H1("Recommended Potential Collaborators", style={'color': 'FireBrick', 'textAlign': 'center'}),
            dbc.Row([
                dash_table.DataTable(
                    id='top-faculty-table',
                    columns=[{"name": "Recommeded Collaborators", "id": "faculty-related-keywords"}],
                    data=[{"faculty-related-keywords": k} for k in get_top10_faculty_related_favorite_keywords()],
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable='single',
                    selected_rows = [],
                    page_size=10,
                    style_cell={'textAlign': 'left', 'font-family': 'Georgia'},
                    style_header={
                        'backgroundColor': 'FireBrick', 'color': 'white', 'textAlign': 'center','font-family': 'Georgia'},
                ),
            ], className='my-3')
        ], width=3),

        ### Widget 5 ###
        dbc.Col([
            html.H1("Collaborator Information", style={'color': 'FireBrick', 'textAlign': 'center'}),
            dbc.Row([
                html.Div(
                    id = "partner-info",
                    )
            ], className='my-3')
        ], width=3),
    ], class_name='p-3 d-flex justify-content-around'),



    ### Row 3 ###
    dbc.Row([
        ### Widget 6 ###
        dbc.Col([
            html.H1("Potential Collaborator Notes", style={'color': 'FireBrick', 'textAlign': 'center'}),
            dbc.Row([
                dash_table.DataTable(
                    id='potential-partner-table',
                    columns=[{"name": "Potential Collaborator", "id": "potential-partner"}, {"name":"Notes", "id": "my-notes"}],
                    data=[{"potential-partner": p, "my-notes": notes} for p, notes in get_notes()],
                    sort_action="native",
                    sort_mode="multi",
                    editable=True,
                    row_deletable=True,
                    page_size=10,
                    style_cell={'textAlign': 'left', 'font-family': 'Georgia'},
                    style_header={
                        'backgroundColor': 'FireBrick', 'color': 'white', 'textAlign': 'center','font-family': 'Georgia'},
                ),
            ], className='my-3'),
            
            dbc.Button('Add Row', id='editing-rows-button', n_clicks=0, color='secondary', className='mr-2'),
            
            
        ], width=3),
        
        ### Widget 7 ###
        dbc.Col([
            html.H1("Networking to Potential Collaborator", style={'color': 'FireBrick', 'textAlign': 'center'}),
            dbc.Row(
                id='connection_finder_widget',
                children=[
                    html.Label('Connection From', style={'font-family': 'Georgia', 'color': 'FireBrick', 'display': 'block',
                                                    'text-align': 'left', 'margin-top': '10px'}),
                    html.Br(),
                    dcc.Dropdown(queryFaculties(),
                                id="faculty_selection_from",
                                style={'font-family': 'Georgia'}),
                    html.Br(),
                    html.Label('Connection To', style={'font-family': 'Georgia', 'color': 'FireBrick',
                                                    'display': 'block', 'text-align': 'left',
                                                    'margin-top': '10px'}),
                        
                    dcc.Dropdown(queryFaculties(), 
                                id="faculty_selection_to",
                                style={'font-family': 'Georgia'}),
                    html.Br(),
                    html.Br(),
                ]),
            dbc.Button('Search', id='connection_search', n_clicks=0, color='secondary', className='mr-2'),
            dbc.Row([html.Div(id="faculty_relation_path")])
        ], width=7, style={'margin-left': '15px'})
            
    
    ], class_name='p-3 d-flex justify-content-around'),

], fluid=True)




# callback for widget 1
@callback(
    Output('keyword-bar', 'figure'),
    Input('year-slider', 'value')
)
def update_graph(year_range):
    df = get_top_10_keywords(year_range[0], year_range[1])
    fig = px.bar(df, x="publication counts", y='keywords' , text_auto='.2s', orientation='h', color="publication counts")
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

# callback for widget 2

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(k):
    df = get_trends(k)
    fig = px.line(df, x='year', y='publications')
    return fig


# callback for widget 3 & 4 - add to potential research interest table and update potential collaborator table
@callback(
    Output('potential-keywords-table', 'data', allow_duplicate=True),
    Output('top-faculty-table', 'data', allow_duplicate=True),
    Input('add-potential-keyword-button', 'n_clicks'),
    State('keyword-dropdown', 'value'),
    State('potential-keywords-table', 'data'),
    prevent_initial_call=True
    
)

def update_potential_keywords_table(n_clicks, selected_keyword, table):
    if n_clicks > 0 and {'Potential Research Keywords': selected_keyword} not in table:
        add_potential_keyword(selected_keyword)
        table.append({'Potential Research Keywords': selected_keyword})
        top_faculty = [{"faculty-related-keywords": k} for k in get_top10_faculty_related_favorite_keywords()]
        #top_university = [{"university-related-keywords": k} for k in get_top10_university_related_favorite_keywords()]
        
        return table, top_faculty
    
    return table, []

# callback for widget 3 & 4 - delete from potential research interest table and update potential collaborator table

@callback(
    Output('potential-keywords-table', 'data', allow_duplicate=True),
    Output('top-faculty-table', 'data', allow_duplicate=True),
    Input('potential-keywords-table', 'data_previous'),
    State('potential-keywords-table', 'data'),
    prevent_initial_call=True
)
def delete_favorite_keyword_callback(previous, current):
    for row in previous:
        if row not in current:
            delete_potential_keyword(row["Potential Research Keywords"])
            top_faculty = [{"faculty-related-keywords": k} for k in get_top10_faculty_related_favorite_keywords()]
    return current, top_faculty



# callback for widget 5
@callback(
    Output('partner-info', 'children'),
    Input('top-faculty-table', 'data'),
    Input('top-faculty-table', 'selected_rows'),
    
)
def update_partner_info(data, selected_rows):
    if selected_rows and selected_rows != [] and data != []:
        id = str(selected_rows[0])
        name = str(data[int(id)]["faculty-related-keywords"])
        return dbc.Card(
            [
                dbc.CardImg(src=get_faculty_info(name)[0][0], style={'textAlign': 'center', "width": "100%", "height":"30vh", "object-fit":"cover", "border-radius": "100%"}),
                dbc.CardBody(
                    [
                        html.H4(get_faculty_info(name)[0][1], style={'color': 'FireBrick', 'textAlign': 'center'}),
                        html.P(get_faculty_info(name)[0][3], style={'color': 'FireBrick', 'textAlign': 'center'}),
                        html.P(get_faculty_info(name)[0][4], style={'color': 'FireBrick', 'textAlign': 'center'}),
                        html.P(get_faculty_info(name)[0][5], style={'color': 'FireBrick', 'textAlign': 'center'}),
                        html.P(get_faculty_info(name)[0][6], style={'color': 'FireBrick', 'textAlign': 'center'}),
                    ]
                ),
                            
                        
        ], style = { "border": '0'}
        )
    return ""
    

# callback for widget 6

@callback(
    Output('potential-partner-table', 'data', allow_duplicate=True),
    Input('editing-rows-button', 'n_clicks'),
    State('potential-partner-table', 'data'),
    State('potential-partner-table', 'columns'),
    prevent_initial_call=True
)

def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
        add_to_notes(rows[-1]["potential-partner"], rows[-1]["my-notes"])
    return rows


@callback(
    Output('potential-partner-table', 'data', allow_duplicate=True),
    Input('potential-partner-table', 'data_previous'),
    State('potential-partner-table', 'data'),
    prevent_initial_call=True
)

def update_notes_table(previous, current):
    for row in current:
        if row not in previous:
            add_to_notes(row["potential-partner"], row["my-notes"])
    
    for row in previous:
        if row not in current:
            delete_from_notes(row["potential-partner"], row["my-notes"])
    return current



# Callback for widget 7
@app.callback(
    Output(component_id='faculty_relation_path', component_property='children'),
    State(component_id='faculty_selection_from', component_property='value'),
    State(component_id='faculty_selection_to', component_property='value'),
    Input(component_id='connection_search', component_property='n_clicks')
)
def update_connections_chart(fromFaculty, toFaculty, n_clicks):
    if n_clicks ==0 or n_clicks is None:
        return no_update
    if fromFaculty is None:
        return html.Label('PLEASE SELECT CONNECTION FROM', className='h3',
                          style={'font-family': 'Georgia', 'text-align': 'center',
                                 'color': 'FireBrick', 'margin-top': '20px'})
    if toFaculty is None:
        return html.Label('PLEASE SELECT CONNECTION TO', className='h3',
                          style={'font-family': 'Georgia', 'text-align': 'center',
                                 'color': 'FireBrick', 'margin-top': '20px'})
    result = getConnectionsToFaculty(fromFaculty, toFaculty)
    
    if result is None or not result:
        return html.Label('NO CONNECTION EXISTS', className='h3',
                          style={'font-family': 'Georgia', 'text-align': 'center',
                                 'color': 'FireBrick', 'margin-top': '20px'})
    else:
        connectionGraph = cyto.Cytoscape(layout={'name': 'breadthfirst'}, elements=result,
                                         style={'width': '90%', 'height': '400px', 'background-color': 'rgba(0,0,0,0)'},
                                         stylesheet=[{'selector': 'label', 'style': {'content': 'data(label)',
                                                                                     'color': 'black',
                                                                                     'font-family': 'Georgia',
                                                                                     'text-justification': 'center',
                                                                                     'background-color': 'FireBrick'}}])
        return connectionGraph



# Run the app
if __name__ == '__main__':
    app.run(debug=True)