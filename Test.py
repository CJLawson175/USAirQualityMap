from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Import data from GitHub (use raw URL)
data_url = 'https://raw.githubusercontent.com/CJLawson175/USAirQualityMap/main/Completed.csv'
data = pd.read_csv(data_url)


# Check and remove any rows with missing latitude or longitude values
data = data.dropna(subset=['Site Latitude', 'Site Longitude'])

# Ensure the 'Year' column is treated as an integer or string (necessary for animation frame)
data['Year'] = data['Year'].astype(str)

# Check if latitudes and longitudes are within valid ranges
if data['Site Latitude'].min() < -90 or data['Site Latitude'].max() > 90:
    print("Warning: Some latitudes are out of range")
if data['Site Longitude'].min() < -180 or data['Site Longitude'].max() > 180:
    print("Warning: Some longitudes are out of range")

app = Dash()



@callback(
    Output('graph-with-slider', 'figure'),
    Input('Year-slider', 'value')
)
def update_figure(selected_Year):
    filtered_data = data[data.Year == selected_Year]

# Create the scatter plot on the US map with dots for each location
fig = px.scatter_geo(data,
                     lat='Site Latitude',  # Latitude for the location
                     lon='Site Longitude',  # Longitude for the location
                     color='Daily Max Concentration',  # Use CO2 concentration for color
                     hover_name='Local Site Name',  # Hover text with the site name
                     hover_data=['State', 'Daily Max Concentration', 'Year'],  # Additional hover info
                     animation_frame='Year',  # Animate based on Year
                     scope='usa',  # Focus the map on the USA
                     title='CO2 Concentration in US States Over Time',
                     color_continuous_scale='Viridis',  # Adjust color scale for better visualization
                     labels={"Daily Max Concentration": "CO2 Concentration (ppm)"},
                     projection="albers usa",  # Use the Albers projection for a more focused USA view
                     opacity=0.6,  # Adjust opacity to make the dots more visible
                     size_max=10,  # Adjust the maximum size of the dots
                    )


# Update the layout to ensure the map renders correctly
fig.update_geos(showland=True, landcolor="lightgray", showlakes=True, lakecolor="lightblue", 
              coastlinecolor="black", showcoastlines=True)

# Show the map
fig.show()
