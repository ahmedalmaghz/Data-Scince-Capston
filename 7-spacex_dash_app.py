# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 10:55:29 2021

@author: AbuEmad
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()
# print(launch_sites)
# launch_sites.append['ALL']
spacex_df.astype({'class': 'int32'})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...CCAFS LC-40,VAFB SLC-4E,KSC LC-39A,CCAFS SLC-40)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 # {'label': site, 'value': site} for site in launch_sites 
                                                ],
                                            value='ALL',
                                            placeholder=" Select a Launch Site here",
                                            searchable=True
                                            ),
                                                            
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: '{}'.format(i) for i in range(0,10000,2500)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df.groupby(spacex_df['class']), values=spacex_df['Launch Site'].value_counts(), 
                        # names=spacex_df['Launch Site'], 
                        title='Total Success Launches By Site ')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, values=filtered_df['class'].value_counts(), 
                        # names=filtered_df['class'], 
                        title='Total Success Launches For Site:'+entered_site)
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
              )
def get_scateer_chart(entered_site,enterd_payload):
    # spacex_df_rs= spacex_df.query(spacex_df['Payload Mass (kg)']>=enterd_payload[0] and spacex_df['Payload Mass (kg)']<=enterd_payload[1])
    filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
    
    if entered_site == 'ALL':
        fig = px.scatter( spacex_df, x='Payload Mass (kg)',y='class',
                          color="Booster Version Category",
                          # names='Scatter chart names', 
                          # size="pop", color="continent",
                          title='Correlation between Payload and Success For All Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.scatter( filtered_df, x='Payload Mass (kg)',y='class',
                          color="Booster Version Category",
                          # names='Scatter chart names'+entered_site, 
                          # size="pop", color="continent",
                          title='Correlation between Payload and Success For Site:'+entered_site)
        return fig
        

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)