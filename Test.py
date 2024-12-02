import plotly.graph_objects as go
import pandas as pd

# Import data from GitHub (use raw URL)
data_url = 'https://raw.githubusercontent.com/CJLawson175/USAirQualityMap/main/Completed.csv'
data = pd.read_csv(data_url)

# Check the first few rows of the data to understand its structure
print(data.head())

# Ensure the 'Year' column is treated as an integer or string (necessary for animation frame)
data['Year'] = data['Year'].astype(str)

# Aggregate the data by state, calculate the average 'Daily Max Concentration' for each state
state_avg_concentration = data.groupby('State')['Daily Max Concentration'].mean().reset_index()

# Create a Choropleth map trace (for the US states)
choropleth = go.Choropleth(
    locations=state_avg_concentration['State'],  # U.S. states
    z=state_avg_concentration['Daily Max Concentration'],  # Average concentration for each state
    hoverinfo='location+z',  # Show location (state) and the average concentration on hover
    locationmode='USA-states',  # Use the USA-states location mode
    colorscale='Viridis',  # Color scale
    colorbar=dict(title="Average CO2 Concentration (ppm)"),  # Label for the color bar
)

# Create a scatter plot trace (for the specific data points)
scatter = go.Scattergeo(
    lat=data['Site Latitude'],  # Latitude for the location
    lon=data['Site Longitude'],  # Longitude for the location
    text=data['Local Site Name'] + "<br>Average CO2 Concentration: " + data['Daily Max Concentration'].astype(str),  # Hover text with the site name and concentration
    hoverinfo='text',  # Show the information on hover
    mode='markers',  # Use markers for dots
    marker=dict(
        size=6,  # Size of the dots
        color=data['Daily Max Concentration'],  # Color based on CO2 concentration
        colorscale='Viridis',  # Color scale
    )
)

# Create a figure and add both the Choropleth and Scatter plot traces
fig = go.Figure(data=[choropleth, scatter])

# Update layout to customize the map appearance and add titles
fig.update_layout(
    geo=dict(
        scope='usa',  # Focus the map on the USA
        projection_type='albers usa',  # Albers USA projection
        showland=True,  # Show land
        landcolor='lightgray',  # Color of land
        showlakes=True,  # Show lakes
        lakecolor='lightblue',  # Color of lakes
        showcoastlines=True,  # Show coastlines
        coastlinecolor='black',  # Color of coastlines
    ),
    title='CO2 Concentration in US States with Specific Locations',
    title_x=0.5,  # Center the title
)

# Show the map
fig.show()
