# United States Air Quality Interavtive Map: Version 1

Source: **[Environmental Protection Agency Data on Air Quality](https://www.epa.gov/outdoor-air-quality-data/download-daily-data)**

Website: **[United States Air Quality Visualization](https://dash-air-quality-app-02617dcbdf3f.herokuapp.com/)**

<h2>Description</h2>
<b>This project is intended to use Python to process large amounts of data from 2020-2024 about Air Quality data in the United States. The goal of this project is to make a user-friendly app through plotly that allows the user to viualize air quality data based on variable color change on a map of the United states with a color chart to determine higher/lower levels. This Project involved a large amount of data processing and Data Visualization, all of the files used for processing are included in this repository. The final step in this Proejct was to use git to deploy the Project through Heroku for an always-open web application. Version 1 of this project is now complete and can be viewed through the provided link.

</b>
<br />

</p>
<h2>Project goals</h2>

- <b>Create a user-friendly, simple to understand visualization of air quality data for CO2, NO2, Ozone, and PM2.5.
- <b>Create a map with each State and a variable color for the average level of a specific pollutant in that region.
- <b>Allow the user to switch between the different pollutants using a selection feature.
- <b>Allow the user to choose which years data to display.
- <b>Use plotly and Dash to create a web-based application.

<h2>Current State of the Application</h2>
<p align="center">
<img src="https://i.imgur.com/itPen5R.png" height="70%" width="70%" alt="RDP event fail logs to iP Geographic information"/>

</p>
<h2>Project Steps</h2>

- <b>Collect Data from the EPA website.
- <b>Create Python scripts to Process and Combine all files into one .csv file.
- <b>Use Plotly.express and pandas libraries to process and visualize data.
    - <b>States and Values were placed into pandas dataframe.
    - <b>"States" column defined as "Locations" in plotly, and USA-States was used to confine map to USA.
- <b>Callback and HTML elements were added using Dash (Dropdown, Slider, map).
- <b>Deployed app onto Heroku using git, and supporting files (requirements.txt, Procfile, etc...).
- <b> App Completed 01/04/2025.

</p>
<h2>What's Next? (Version 2)</h2>

- <b>Add location marker for every data site on the nation using Scatterplot and .csv latitude/longitude.
- <b>Scrape more data to extend the range of data.
