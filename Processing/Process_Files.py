import pandas as pd
import os

# Load the data from the CSV file
file_path = r'C:\Users\Charl\Downloads\Data\Filtered raw\Filtered46-50.csv'  # Path to your input CSV file
output_file_path = r'C:\Users\Charl\Downloads\Data\FilteredDone\Filtered46-50.csv'  # Path to save the filtered output

# Define the mapping for pollutants
pollutant_mapping = {
    'Carbon monoxide': 'CO2 (ppm)',
    'Ozone': 'Ozone (ppm)',
    'Nitrogen dioxide (NO2)': 'NO2 (ppb)'
}

# Fallback for any other pollutant not specifically mapped
default_pollutant = 'PM2.5 (ug/m3)'

# Define the state abbreviation mapping
state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Check if the file exists
if not os.path.exists(file_path):
    print(f"The file does not exist: {file_path}")
else:
    # Try to read the CSV file
    try:
        df = pd.read_csv(file_path)
        print(f"Original DataFrame shape: {df.shape}")  # Show original shape of DataFrame
        print("Original DataFrame head:\n", df.head())  # Check the first few rows

        # Specify the columns to filter
        co2_column_name = 'Daily Max Concentration'  # The CO2 column to check
        percent_complete_column_name = 'Percent Complete'  # The Percent Complete column to check

        # Check if the specified columns exist
        if co2_column_name not in df.columns or percent_complete_column_name not in df.columns:
            print(f"One or both columns not found in the DataFrame.")
        else:
            # Filter the DataFrame to keep only rows where:
            # 1. Daily Max 8-hour CO2 Concentration is greater than or equal to 0
            # 2. Percent Complete is greater than or equal to 90
            filtered_df = df[(df[co2_column_name] >= 0) & (df[percent_complete_column_name] >= 90)]

            # Specify the columns to keep (modify this if you want to include more or different columns)
            columns_to_keep = ["Date", "Daily Max Concentration", "Units", "Daily AQI Value", 
                               "Local Site Name", "AQS Parameter Description", "State", "County", 
                               "Site Latitude", "Site Longitude"]

            # Keep only the specified columns
            filtered_df = filtered_df[columns_to_keep]

            # Split the 'Date' column into 'Year', 'Month', and 'Day'
            filtered_df['Year'] = pd.to_datetime(filtered_df['Date'], format='%m/%d/%Y').dt.year
            filtered_df['Month'] = pd.to_datetime(filtered_df['Date'], format='%m/%d/%Y').dt.month

            # Map the AQS Parameter Description values to the desired pollutant names
            filtered_df['Pollutant'] = filtered_df['AQS Parameter Description'].map(pollutant_mapping).fillna(default_pollutant)

            # Now, create a column for each pollutant
            # Initialize the new pollutant columns for each mapped pollutant
            pollutants = ['CO2 (ppm)', 'Ozone (ppm)', 'NO2 (ppb)', 'PM2.5 (ug/m3)']
            for pollutant in pollutants:
                filtered_df[pollutant] = None  # Start with empty columns

            # Populate each pollutant's column with the corresponding Daily Max Concentration
            for index, row in filtered_df.iterrows():
                pollutant_column = row['Pollutant']
                filtered_df.at[index, pollutant_column] = row[co2_column_name]

            # Step 1: Convert pollutant columns to numeric (coerce errors to NaN)
            filtered_df['CO2 (ppm)'] = pd.to_numeric(filtered_df['CO2 (ppm)'], errors='coerce')
            filtered_df['Ozone (ppm)'] = pd.to_numeric(filtered_df['Ozone (ppm)'], errors='coerce')
            filtered_df['NO2 (ppb)'] = pd.to_numeric(filtered_df['NO2 (ppb)'], errors='coerce')
            filtered_df['PM2.5 (ug/m3)'] = pd.to_numeric(filtered_df['PM2.5 (ug/m3)'], errors='coerce')
            filtered_df['Daily AQI Value'] = pd.to_numeric(filtered_df['Daily AQI Value'], errors='coerce')

            # Step 2: Handle NaN values by filling with 0 and then replacing 0 with NaN
            filtered_df['CO2 (ppm)'].fillna(0, inplace=True)
            filtered_df['Ozone (ppm)'].fillna(0, inplace=True)
            filtered_df['NO2 (ppb)'].fillna(0, inplace=True)
            filtered_df['PM2.5 (ug/m3)'].fillna(0, inplace=True)
            filtered_df['Daily AQI Value'].fillna(0, inplace=True)

            # Replace all 0 values with NaN to make cells empty
            filtered_df['CO2 (ppm)'] = filtered_df['CO2 (ppm)'].replace(0, float('nan'))
            filtered_df['Ozone (ppm)'] = filtered_df['Ozone (ppm)'].replace(0, float('nan'))
            filtered_df['NO2 (ppb)'] = filtered_df['NO2 (ppb)'].replace(0, float('nan'))
            filtered_df['PM2.5 (ug/m3)'] = filtered_df['PM2.5 (ug/m3)'].replace(0, float('nan'))
            filtered_df['Daily AQI Value'] = filtered_df['Daily AQI Value'].replace(0, float('nan'))

            # Group by Year, Month, and Local Site Name, and calculate the average for each pollutant
            grouped_df = filtered_df.groupby(['Year', 'Month', 'Local Site Name', 'State'], as_index=False).agg({
                'CO2 (ppm)': 'mean',  # Calculate average for CO2
                'Ozone (ppm)': 'mean',  # Calculate average for Ozone
                'NO2 (ppb)': 'mean',  # Calculate average for NO2
                'PM2.5 (ug/m3)': 'mean',  # Calculate average for PM2.5
                'Daily AQI Value': 'mean',  # Calculate average for Daily AQI Value
                'Site Latitude': 'first',  # Take the first value for Site Latitude
                'Site Longitude': 'first'  # Take the first value for Site Longitude
            })

            # Apply the state abbreviation mapping
            grouped_df['State'] = grouped_df['State'].map(state_abbreviations)

            # Remove any duplicate rows
            grouped_df = grouped_df.drop_duplicates()

            # Specify the final columns to retain: Year, Month, Local Site Name, State, and the pollutants
            final_columns = ['Year', 'Month', 'Local Site Name', 'State', 
                             'CO2 (ppm)', 'Ozone (ppm)', 'NO2 (ppb)', 'PM2.5 (ug/m3)', 
                             'Daily AQI Value', 'Site Latitude', 'Site Longitude']

            # Final DataFrame
            final_df = grouped_df[final_columns]

            # Save the final DataFrame to a new CSV file
            final_df.to_csv(output_file_path, index=False)
            print(f"Filtered data saved to: {output_file_path}")

    except Exception as e:
        print(f"Error processing the file: {e}")
