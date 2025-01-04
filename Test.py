import pandas as pd
import plotly.express as px
import dash
import dash_table  # Import the dash_table module
from dash import dcc, html, Input, Output
from flask import Flask

# Import data from GitHub (use raw URL)
data_url = 'https://raw.githubusercontent.com/CJLawson175/USAirQualityMap/main/ENG220_Data_Filtered.csv'
df = pd.read_csv(data_url)

# Ensure the 'Year' column is treated as an integer or string (necessary for animation frame)
df['Year'] = df['Year'].astype(str)

# Calculate the yearly average, max, and min CO2 (ppm) per state
state_stats = df.groupby(['Year', 'State'])['CO2 (ppm)'].agg(['mean', 'max']).reset_index()

# Round the average and max CO2 values to 3 decimals
state_stats['mean'] = state_stats['mean'].round(3)
state_stats['max'] = state_stats['max'].round(3)

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app and link it to Flask server
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')

# Layout
app.layout = html.Div([
    # Map section
    dcc.Graph(
        id='my_map',  # Graph to display the map
        style={'height': '80vh'},  # Make the map take 80% of the vertical height of the viewport
        config={'modeBarButtonsToRemove': ['Pan', 'Downloadplotasapng', 'BoxSelect', 'LassoSelect']},
    ),

    # Slider and text output section
    html.Div([
        dcc.Slider(
            id='my_slider',  # Correct the ID here
            min=int(df['Year'].min()),  # Set min to the earliest year
            max=int(df['Year'].max()),  # Set max to the latest year
            value=int(df['Year'].max()),  # Default to the latest year
            marks={year: str(year) for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1)},
            step=1,
        ),
        html.Div(id='slider-output-container'),  # Container to show year
    ], style={'padding': '20px', 'textAlign': 'center'}),  # Add some padding around the slider and center it

    # Section to display the first few rows of filtered data
    html.Div(id='filtered-data-table', style={'padding': '20px'})
])

# Callback to update the map and the output container based on the slider
@app.callback(
    [Output('slider-output-container', 'children'),
     Output('my_map', 'figure'),  # Update the map figure
     Output('filtered-data-table', 'children')],  # Output for filtered data table
    Input('my_slider', 'value')  # Listen to slider changes
)
def update_figure(selected_Year):
    # Filter the data based on the selected year
    dff = state_stats[state_stats['Year'] == str(selected_Year)]

    # Create the choropleth map for average CO2 (ppm)
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='State',  # Use 'State' column for locations
        scope="usa",
        color='mean',  # Color by average CO2 concentration
        range_color = [0,0.2],
        hover_data=['Year', 'mean', 'max'],  # Additional hover info for average and max CO2
        color_continuous_scale="Viridis",  # Choose an appropriate color scale
        labels={'mean': 'Average CO2 Concentration (ppm)', 'max': 'Max CO2 Concentration (ppm)'},
    )

    # Update the layout to ensure the map renders correctly
    fig.update_geos(
        showland=True, 
        landcolor="lightgray", 
        showlakes=True, 
        lakecolor="lightblue", 
        coastlinecolor="black", 
        showcoastlines=True
    )

    # Prepare the data for the table (first few rows)
    table = dash_table.DataTable(
        data=dff.head().to_dict('records'),  # Convert the first few rows to a dictionary for the DataTable
        columns=[
            {'name': 'Year', 'id': 'Year'},
            {'name': 'State', 'id': 'State'},
            {'name': 'Average CO2 (ppm)', 'id': 'mean'},
            {'name': 'Max CO2 (ppm)', 'id': 'max'},
        ],  # Define the columns based on the DataFrame's columns
        style_table={'overflowX': 'auto'},  # Allow horizontal scrolling if the table is too wide
        style_cell={'textAlign': 'left', 'padding': '10px'},  # Style the cells
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},  # Style the header
    )

    # Return the updated text (year), map figure, and the first few rows of filtered data
    return f"", fig, table

# Route for the home page
@server.route('/')
def home():
    return 'Welcome to the Flash app! <a href="/dash/">Go to the Dash app</a>'

app.run()
