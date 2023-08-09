import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import base64
from plotly import graph_objects as go

# Loading the Excel file
excel_path = "C:\\Users\\rasis.ritonga\\Downloads\\Database.xlsx"

# URL of the LUX theme from Bootswatch
LUX_theme_url = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/lux/bootstrap.min.css"
external_stylesheets = [LUX_theme_url]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# Read GHG Data for dropdown options
ghg_data = pd.read_excel(excel_path, 'GHG Data')
ghg_data['Date'] = pd.to_datetime(ghg_data['Date'], unit='D', origin='1899-12-30')
sites_options = [{'label': 'All', 'value': 'All'}] + [{'label': site, 'value': site} for site in ghg_data['Site'].unique()]
treatment_options = [{'label': 'All', 'value': 'All'}] + [{'label': treatment, 'value': treatment} for treatment in ghg_data['Treatment'].unique()]
type_options = [{'label': 'All', 'value': 'All'}] + [{'label': type_, 'value': type_} for type_ in ghg_data['Type'].unique()]

# Read AWS Data and convert Date
aws_data = pd.read_excel(excel_path, 'AWS Data')
aws_data['Date'] = pd.to_datetime(aws_data['Date'], unit='D', origin='1899-12-30')

# Read Carbon AGB Data
carbon_agb_data = pd.read_excel(excel_path, 'Carbon_AGB')

# Read Carbon BGB Data
carbon_bgb_data = pd.read_excel(excel_path, 'Carbon_BGB')

# Graph style
graph_style = {'color': '#007BFF'}  # Dark blue color used in the LUX theme

# Function to encode image
def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return f'data:image/png;base64,{encoded.decode()}'

# Logo paths
logo1_path = "C:\\Users\\rasis.ritonga\\Downloads\\logo1.png"
logo2_path = "C:\\Users\\rasis.ritonga\\Downloads\\logo2.png"

# Main layout
app.layout = html.Div([
    # Navbar
    html.Nav([
        html.Div([
            # Logos and Title Section
            html.Div([
                # Two logos side by side
                html.Div([
                    html.Img(src=encode_image(logo1_path), style={'height': '40px'}),
                    html.Img(src=encode_image(logo2_path), style={'height': '40px'}),
                ], style={'display': 'inline-block'}),
                # Dashboard Title
                html.Div([
                    html.H2("NCS Data Hub (Plug & Play Version)", style={'color': '#333'})
                ], style={'display': 'inline-block', 'marginLeft': '20px'}),
            ], style={'marginBottom': '20px'}),  # Added vertical space here
            # Tabs Section
            dcc.Tabs(id='tabs', value='tab-ghg', children=[
                dcc.Tab(label='GHG Data', value='tab-ghg'),
                dcc.Tab(label='AWS Data', value='tab-aws'),
                dcc.Tab(label='Carbon AGB', value='tab-agb'),
                dcc.Tab(label='Carbon BGB', value='tab-bgb')
            ], className='tabs-container')
        ], className='navbar')
    ]),
    html.Div(id='tabs-content', style={'padding': '20px'})
], style={'margin': '20px'})

# Unique options for Region and Site in Carbon AGB Data
agb_region_options = [{'label': region, 'value': region} for region in carbon_agb_data['Region'].unique()]
agb_site_options = [{'label': site, 'value': site} for site in carbon_agb_data['Site'].unique()]

# Callback to update the content of the selected tab
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    # GHG Data Tab
    if tab == 'tab-ghg':
        return html.Div([
            html.H3('GHG Data Visualization', style={'textAlign': 'center'}),
            # Filters
            html.Div([
                html.Div([
                    html.Label('Select Site:'),
                    dcc.Dropdown(
                        id='site-dropdown',
                        options=sites_options,
                        value='All',  # Default value
                        style={'width': '100%'}
                    ),
                ], style={'width': '32%', 'display': 'inline-block'}),
                html.Div([
                    html.Label('Select Treatment:'),
                    dcc.Dropdown(
                        id='treatment-dropdown',
                        options=treatment_options,
                        value='All'  # Default value
                    ),
                ], style={'width': '32%', 'display': 'inline-block'}),
                html.Div([
                    html.Label('Select Type:'),
                    dcc.Dropdown(
                        id='type-dropdown',
                        options=type_options,
                        value='All'  # Default value
                    ),
                ], style={'width': '32%', 'display': 'inline-block'}),
            ], style={'margin-bottom': '20px'}),
            # CO2 Section
            html.Div([
                html.Label('CO2 Data Distribution:'),
                dcc.Dropdown(
                    id='co2-distribution-dropdown',
                    options=[
                        {'label': 'Daily', 'value': 'D'},
                        {'label': 'Biweekly', 'value': '2W'},
                        {'label': 'Monthly', 'value': 'M'}
                    ],
                    value='D'  # Default value
                ),
                html.Div(id='co2-graph')
            ], style={'margin-bottom': '40px'}),
            # CH4 Section
            html.Div([
                html.Label('CH4 Data Distribution:'),
                dcc.Dropdown(
                    id='ch4-distribution-dropdown',
                    options=[
                        {'label': 'Daily', 'value': 'D'},
                        {'label': 'Biweekly', 'value': '2W'},
                        {'label': 'Monthly', 'value': 'M'}
                    ],
                    value='D'  # Default value
                ),
                html.Div(id='ch4-graph')
            ])
        ])

    # AWS Data Tab
    elif tab == 'tab-aws':
        return html.Div([
            html.H3('AWS Data Visualization', style={'textAlign': 'center'}),
            html.Label('Select Data Distribution:'),
            dcc.Dropdown(
                id='aws-distribution-dropdown',
                options=[
                    {'label': 'Hourly', 'value': 'H'},
                    {'label': 'Daily', 'value': 'D'},
                    {'label': 'Weekly', 'value': 'W'},
                    {'label': 'Monthly', 'value': 'M'}
                ],
                value='D'  # Default value
            ),
            html.Div(id='aws-graphs')
        ])

    # Carbon AGB Tab
    elif tab == 'tab-agb':
        return html.Div([
            html.H3('Carbon AGB Visualization', style={'textAlign': 'center'}),
            html.Label('Select Region:'),
            dcc.Dropdown(
                id='agb-region-dropdown',
                options=agb_region_options,
                value=None  # Default value
            ),
            html.Label('Select Site:'),
            dcc.Dropdown(
                id='agb-site-dropdown',
                options=agb_site_options,
                value=None  # Default value
            ),
            html.Label('Select Attribute:'),
            dcc.Dropdown(
                id='agb-attribute-dropdown',
                options=[
                    {'label': 'dbh', 'value': 'dbh'},
                    {'label': 'Wood density (g cm3)', 'value': 'Wood density (g cm3)'},
                    {'label': 'TAGB (kg) (Chave, 2005)', 'value': 'TAGB (kg) (Chave, 2005)'},
                    {'label': 'TAGB (kg) (Manuri, 2014)', 'value': 'TAGB (kg) (Manuri, 2014)'},
                    {'label': 'TAGB', 'value': 'TAGB'},
                    {'label': 'C', 'value': 'C'}
                ],
                value='dbh'  # Default value
            ),
            html.Label('Select Category:'),
            dcc.Dropdown(
                id='agb-category-dropdown',
                options=[
                    {'label': 'Spp_Sci', 'value': 'Spp_Sci'},
                    {'label': 'Fam', 'value': 'Fam'}
                ],
                value='Spp_Sci'  # Default value
            ),
            dcc.Graph(id='agb-boxplot')
        ])


    # Carbon BGB Tab
    elif tab == 'tab-bgb':
        return html.Div([
            html.H3('Carbon BGB Visualization', style={'textAlign': 'center'}),
            html.Label('Select Attribute:'),
            dcc.Dropdown(
                id='bgb-attribute-dropdown',
                options=[
                    {'label': 'Depth', 'value': 'Depth'},
                    {'label': 'Depth of sample', 'value': 'Depth of sample'},
                    {'label': 'BD (g/cm3)', 'value': 'BD (g/cm3)'},
                    {'label': '%C', 'value': '%C'},
                    {'label': '%N', 'value': '%N'},
                    {'label': 'C Mg/ha', 'value': 'C Mg/ha'},
                    {'label': 'N Mg/ha', 'value': 'N Mg/ha'},
                    {'label': 'C Mg/ha (peat layers only)', 'value': 'C Mg/ha (peat layers only)'},
                    {'label': 'N Mg/ha (peat layers only)', 'value': 'N Mg/ha (peat layers only)'}
                ],
                value='Depth'  # Default value
            ),
            html.Label('Select Category:'),
            dcc.Dropdown(
                id='bgb-category-dropdown',
                options=[
                    {'label': 'Region', 'value': 'Region'},
                    {'label': 'Land cover', 'value': 'Land cover'},
                    {'label': 'Site', 'value': 'Site'}
                ],
                value='Region'  # Default value
            ),
            dcc.Graph(id='bgb-boxplot')
        ])

# Function to create summary boxes
def summary_boxes(data, title):
    avg_value = round(data.mean(), 2)
    cumulative_value = round(data.sum(), 2)
    num_of_data = len(data)
    return html.Div([
        html.Div([
            html.H4(f'Average {title}'),
            html.P(f'{avg_value}', style={'fontSize': '24px'}),
        ], style={'border': '1px solid #ddd', 'padding': '15px', 'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div([
            html.H4(f'Cumulative {title}'),
            html.P(f'{cumulative_value}', style={'fontSize': '24px'}),
        ], style={'border': '1px solid #ddd', 'padding': '15px', 'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div([
            html.H4(f'Number of Data'),
            html.P(f'{num_of_data}', style={'fontSize': '24px'}),
        ], style={'border': '1px solid #ddd', 'padding': '15px', 'width': '30%', 'display': 'inline-block', 'textAlign': 'center'}),
    ], style={'marginBottom': '20px'})

# Callback to update CO2 graph based on selected filters
@app.callback(
    Output('co2-graph', 'children'),
    Input('site-dropdown', 'value'),
    Input('treatment-dropdown', 'value'),
    Input('type-dropdown', 'value'),
    Input('co2-distribution-dropdown', 'value')
)
def update_co2_graph(selected_site, selected_treatment, selected_type, distribution):
    filtered_data = apply_filters(selected_site, selected_treatment, selected_type)
    resampled_data = filtered_data.resample(distribution, on='Date').mean()
    fig = go.Figure(data=go.Scatter(x=resampled_data.index, y=resampled_data['CO2'],
                                    mode='lines+markers', line=dict(color=graph_style['color'])))
    fig.update_layout(title='CO2 Over Time')
    summary = summary_boxes(resampled_data['CO2'], 'CO2')
    return [summary, dcc.Graph(figure=fig)]

# Callback to update CH4 graph based on selected filters
@app.callback(
    Output('ch4-graph', 'children'),
    Input('site-dropdown', 'value'),
    Input('treatment-dropdown', 'value'),
    Input('type-dropdown', 'value'),
    Input('ch4-distribution-dropdown', 'value')
)
def update_ch4_graph(selected_site, selected_treatment, selected_type, distribution):
    filtered_data = apply_filters(selected_site, selected_treatment, selected_type)
    resampled_data = filtered_data.resample(distribution, on='Date').mean()
    fig = go.Figure(data=go.Scatter(x=resampled_data.index, y=resampled_data['CH4'],
                                    mode='lines+markers', line=dict(color=graph_style['color'])))
    fig.update_layout(title='CH4 Over Time')
    summary = summary_boxes(resampled_data['CH4'], 'CH4')
    return [summary, dcc.Graph(figure=fig)]

# Callback to update AWS Data graphs based on selected distribution
@app.callback(
    Output('aws-graphs', 'children'),
    Input('aws-distribution-dropdown', 'value')
)
def update_aws_graphs(distribution):
    resampled_data = aws_data.resample(distribution, on='Date').mean()
    return [
        html.H5('Relative Humidity Over Time'),
        dcc.Graph(
            figure={'data': [{'x': resampled_data.index, 'y': resampled_data['RH, %'], 'mode': 'markers', 'name': 'Relative Humidity', 'marker': graph_style}],
                    'layout': {'title': 'Relative Humidity Over Time'}}),
        html.H5('Rain Over Time'),
        dcc.Graph(
            figure={'data': [{'x': resampled_data.index, 'y': resampled_data['Rain, mm'], 'type': 'line', 'name': 'Rain', 'line': graph_style}],
                    'layout': {'title': 'Rain Over Time'}}),
        html.H5('Temperature Over Time'),
        dcc.Graph(
            figure={'data': [{'x': resampled_data.index, 'y': resampled_data['Temp, °C'], 'mode': 'markers', 'name': 'Temperature', 'marker': graph_style}],
                    'layout': {'title': 'Temperature Over Time'}})
    ]

# Function to apply filters based on selected site, treatment, and type
def apply_filters(selected_site, selected_treatment, selected_type):
    filtered_data = ghg_data
    if selected_site != 'All':
        filtered_data = filtered_data[filtered_data['Site'] == selected_site]
    if selected_treatment != 'All':
        filtered_data = filtered_data[filtered_data['Treatment'] == selected_treatment]
    if selected_type != 'All':
        filtered_data = filtered_data[filtered_data['Type'] == selected_type]
    return filtered_data

# Callback to update Carbon AGB boxplot
@app.callback(
    Output('agb-boxplot', 'figure'),
    Input('agb-region-dropdown', 'value'),
    Input('agb-site-dropdown', 'value'),
    Input('agb-attribute-dropdown', 'value'),
    Input('agb-category-dropdown', 'value')
)
def update_agb_boxplot(selected_region, selected_site, selected_attribute, selected_category):
    filtered_data = carbon_agb_data
    if selected_region:
        filtered_data = filtered_data[filtered_data['Region'] == selected_region]
    if selected_site:
        filtered_data = filtered_data[filtered_data['Site'] == selected_site]
    fig = px.box(filtered_data, x=selected_category, y=selected_attribute, title=f'{selected_attribute} Distribution by {selected_category}')
    return fig

# Callback to update Carbon BGB boxplot
@app.callback(
    Output('bgb-boxplot', 'figure'),
    Input('bgb-attribute-dropdown', 'value'),
    Input('bgb-category-dropdown', 'value')
)
def update_bgb_boxplot(selected_attribute, selected_category):
    fig = px.box(carbon_bgb_data, x=selected_category, y=selected_attribute, title=f'{selected_attribute} Distribution by {selected_category}')
    return fig

# To run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
