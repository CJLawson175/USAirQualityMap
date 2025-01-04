from dash import Dash, dcc, html, dash_table, Input, Output
from dash.dash_table.Format import Group
import pandas as pd
import plotly.express as px
import os  # For reading environment variables

# Import data from GitHub
data_url = 'https://raw.githubusercontent.com/CJLawson175/USAirQualityMap/main/USAirQualityData.csv'
df = pd.read_csv(data_url)

df['Year'] = df['Year'].astype(str)

# List of columns that are toxins
exclude_columns = ['Month', 'Local Site Name', 'Site Latitude', 'Site Longitude', 'Year', 'State']
toxins = [col for col in df.columns if col not in exclude_columns]

# Initialize the Dash app
app = Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    # Dropdown to select the type of toxin
    html.Div([
        dcc.Dropdown(
            id='toxins-dropdown',  # Dropdown ID
            options=[{'label': toxin, 'value': toxin} for toxin in toxins],
            value='CO2 (ppm)',  # Default value
            style={'width': '50%'}
        ),
    ], style={'padding': '20px', 'textAlign': 'center'}),

    # Map section
    dcc.Graph(
        id='my_map',  # ID Graph to display the map
        style={'height': '80vh'},
        config={'modeBarButtonsToRemove': ['Pan', 'Downloadplotasapng', 'BoxSelect', 'LassoSelect']},
    ),

    # Slider and text output section
    html.Div([
        dcc.Slider(
            id='my_slider',
            min=int(df['Year'].min()),  # Set min
            max=int(df['Year'].max()),  # Set max
            value=int(df['Year'].max()),  # Default to the latest year
            marks={year: str(year) for year in range(int(df['Year'].min()), int(df['Year'].max()) + 1)},
            step=1,
        ),
        html.Div(id='slider-output-container'),  #show year
    ], style={'padding': '20px', 'textAlign': 'center'}),  # Add padding around the slider and center
])

# Callback to update the map and the output container based on slider and dropdown
@app.callback(
    [Output('slider-output-container', 'children'),
     Output('my_map', 'figure')],  # Update the map figure only
    [Input('my_slider', 'value'),  # Look for slider changes
     Input('toxins-dropdown', 'value')]  # Look for dropdown changes
)
def update_figure(selected_Year, selected_toxin):
    # Filter the data based on the selected year
    dff = df[df['Year'] == str(selected_Year)]

    # Calculate the yearly average, max, and min for the selected toxin
    state_stats = dff.groupby(['Year', 'State'])[selected_toxin].agg(['mean', 'max']).reset_index()

    # Round the average and max toxin values to 3 decimals
    state_stats['mean'] = state_stats['mean'].round(3)
    state_stats['max'] = state_stats['max'].round(3)

    # Create the choropleth map for the selected toxin
    fig = px.choropleth(
        data_frame=state_stats,
        locationmode='USA-states',
        locations='State',  # Use 'State' column for locations
        scope="usa",
        color='mean',  # Color by average toxin concentration
        range_color=[state_stats['mean'].min(), state_stats['mean'].max()],
        hover_data=['mean', 'max'],  #hover info for average and max toxin
        color_continuous_scale="Viridis",  #color scale
        labels={'mean': f'Average {selected_toxin}', 'max': f'Max {selected_toxin}'},
    )

    # Update the layout to render
    fig.update_geos(
        showland=True,
        landcolor="lightgray",
        showlakes=True,
        lakecolor="lightblue",
        coastlinecolor="black",
        showcoastlines=True
    )

    # Return the updated text and map figure
    return f"Year: {selected_Year}", fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
