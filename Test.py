from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Import data from GitHub (use raw URL)
data_url = 'https://raw.githubusercontent.com/CJLawson175/USAirQualityMap/main/Completed.csv'
df = pd.read_csv(data_url)

# Check and remove any rows with missing latitude or longitude values
df = df.dropna(subset=['Site Latitude', 'Site Longitude'])

# Ensure the 'Year' column is treated as an integer or string (necessary for animation frame)
df['Year'] = df['Year'].astype(str)

# Check if latitudes and longitudes are within valid ranges
if df['Site Latitude'].min() < -90 or df['Site Latitude'].max() > 90:
    print("Warning: Some latitudes are out of range")
if df['Site Longitude'].min() < -180 or df['Site Longitude'].max() > 180:
    print("Warning: Some longitudes are out of range")

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    # Map section
    dcc.Graph(
        id='my_map',  # Graph to display the map
        style={'height': '80vh'},  # Make the map take 80% of the vertical height of the viewport
        config = {'modeBarButtonsToRemove': ['Pan', 'Downloadplotasapng', 'BoxSelect', 'LassoSelect'],},
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
    ], style={'padding': '20px', 'textAlign': 'center'})  # Add some padding around the slider and center it
])

# Callback to update the map and the output container based on the slider
@app.callback(
    [Output('slider-output-container', 'children'),
     Output('my_map', 'figure')],  # Update the map figure
    Input('my_slider', 'value')  # Listen to slider changes
)
def update_figure(selected_Year):
    # Filter the data based on the selected year
    filtered_data = df[df['Year'] == str(selected_Year)]

    # Create the scatter plot on the US map with dots for each location
    fig = px.scatter_geo(filtered_data,
                         lat='Site Latitude',  # Latitude for the location
                         lon='Site Longitude',  # Longitude for the location
                         color='Daily Max Concentration',  # Use CO2 concentration for color
                         hover_name='Local Site Name',  # Hover text with the site name
                         hover_data=['State', 'Daily Max Concentration', 'Year'],  # Additional hover info
                         scope='usa',  # Focus the map on the USA
                         title=f'CO2 Concentration in US States for {selected_Year}',  # Title with selected year
                         color_continuous_scale='Viridis',  # Adjust color scale for better visualization
                         range_color = [0,3],
                         labels={"Daily Max Concentration": "CO2 Concentration (ppm)"},
                         projection="albers usa",  # Use the Albers projection for a more focused USA view
                         opacity=0.6,  # Adjust opacity to make the dots more visible
                         size_max=10,  # Adjust the maximum size of the dots
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

    # Return the updated text and figure
    return f"The year chosen by user was: {selected_Year}", fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
