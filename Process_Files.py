import pandas as pd
import os

# Load the data from the CSV file
file_path = r'C:\AirQualityProject\Filtered.csv'  # Path to your input CSV file
output_file_path = r'C:\AirQualityProject\Completed.csv'  # Path to save the filtered output

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

            # Split the 'Date' column into 'Year' and 'Month'
            filtered_df['Year'] = pd.to_datetime(filtered_df['Date'], format='%m/%d/%Y').dt.year
            filtered_df['Month'] = pd.to_datetime(filtered_df['Date'], format='%m/%d/%Y').dt.month

            print(f"Filtered DataFrame shape after adding Year and Month: {filtered_df.shape}")  # Show shape of filtered DataFrame
            print("Filtered DataFrame head with Year and Month:\n", filtered_df.head())  # Check the first few rows of filtered data

            # Save the filtered DataFrame to a new CSV file
            filtered_df.to_csv(output_file_path, index=False)
            print(f"Filtered data saved to: {output_file_path}")

    except Exception as e:
        print(f"Error processing the file: {e}")
