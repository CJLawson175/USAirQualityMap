# Import necessary libraries
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os  # For reading environment variables

# Your data URL or local file path
data_url = 'https://raw.githubusercontent.com/CJLawson175/USAirQualityMap/main/USAirQualityData.csv'
df = pd.read_csv(data_url)

# Ensure the 'Year' column is treated as an integer or string (necessary for animation frame)
df['Year'] = df['Year'].astype(str)

# List of columns that are toxins
exclude_columns = ['Month', 'Local Site Name', 'Site Latitude', 'Site Longitude', 'Year', 'State']
toxins = [col for col in df.columns if col not in exclude_columns]

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='toxins-dropdown',
            options=[{'label': toxin, 'value': toxin} for toxin in toxins],
            value='CO2 (ppm)',  # Default value
            style={'width': '50%'}
        ),
    ], style={'padding': '20px', 'textAlign': 'center'}),

    # The map that will show air quality data
    dcc.Graph(id='my_map', style={'height': '80vh'}, config={'modeBarButtonsToRemove': ['Pan', 'Downloadplotasapng', 'BoxSelect', 'LassoSelect']}),

    # Slider for selecting the year
    html.Div([
        dcc.Slider(
            id='my_slider',
            min=int(df['Year'].min()),
            max=int(df['Year'].max()),
            value=int(df['Year'].max()),  # Default to the latest year
            marks={year: str(year) for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1)},
            step=1,
        ),
        html.Div(id='slider-output-container'),
    ], style={'padding': '20px', 'textAlign': 'center'}),
])

# Define the callback to update the map based on year and toxin type
@app.callback(
    [Output('slider-output-container', 'children'),
     Output('my_map', 'figure')],
    [Input('my_slider', 'value'),
     Input('toxins-dropdown', 'value')]
)
def update_figure(selected_Year, selected_toxin):
    dff = df[df['Year'] == str(selected_Year)]
    state_stats = dff.groupby(['Year', 'State'])[selected_toxin].agg(['mean', 'max']).reset_index()
    state_stats['mean'] = state_stats['mean'].round(3)
    state_stats['max'] = state_stats['max'].round(3)

    # Create the choropleth map
    fig = px.choropleth(
        data_frame=state_stats,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color='mean',
        range_color=[state_stats['mean'].min(), state_stats['mean'].max()],
        hover_data=['mean', 'max'],
        color_continuous_scale="Viridis",
        labels={'mean': f'Average {selected_toxin}', 'max': f'Max {selected_toxin}'},
    )

    fig.update_geos(
        showland=True, 
        landcolor="lightgray", 
        showlakes=True, 
        lakecolor="lightblue", 
        coastlinecolor="black", 
        showcoastlines=True
    )

    return f"Year: {selected_Year}", fig

# The app object is callable (important for Gunicorn)
if __name__ == '__main__':
    app.run_server(debug=True)  # Use this for local testing
