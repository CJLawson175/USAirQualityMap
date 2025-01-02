import os
import pandas as pd

# Specify the folder containing the .csv files
input_folder_path = r'C:\Users\Charl\Downloads\Data\FilteredDone'  # Folder containing .csv files
output_file_path = r'C:\Users\Charl\Downloads\Data\USAirQualityData.csv'  # Output CSV file path

# List to hold DataFrames
dataframes = []

# Check if the input folder exists
if not os.path.exists(input_folder_path):
    print(f"The folder '{input_folder_path}' does not exist. Please check the path.")
else:
    # Loop through all files in the specified input folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.csv'):
            # Construct full file path
            file_path = os.path.join(input_folder_path, filename)
            print(f"Reading file: {file_path}")  # Debugging output
            
            try:
                # Read the csv file into a DataFrame
                df = pd.read_csv(file_path)
                # Check if the DataFrame is empty
                if df.empty:
                    print(f"The file {filename} is empty. Skipping this file.")
                else:
                    # Check if the file has at least 5 columns, and rename the 5th column
                    if len(df.columns) >= 5:
                        df.columns.values[4] = "CO2 (ppm)"
                        print(f"Renamed 5th column in {filename} to 'Daily Max Concentration'.")
                    else:
                        print(f"The file {filename} does not have 5 columns. Skipping renaming.")
                    
                    # Append the DataFrame to the list
                    dataframes.append(df)
                    print(f"Successfully read {filename} with {df.shape[0]} rows and {df.shape[1]} columns.")  # Success message for each file
            except Exception as e:
                print(f"Error processing {filename}: {e}")  # Print error if reading fails

    # Check if there are any DataFrames to combine
    if dataframes:
        # Concatenate all DataFrames in the list into a single DataFrame
        try:
            combined_df = pd.concat(dataframes, ignore_index=True)
            print(f"Combined DataFrame shape: {combined_df.shape}")  # Show shape of combined DataFrame

            # Save the combined DataFrame to a new CSV file
            combined_df.to_csv(output_file_path, index=False)
            print(f"All CSV files in '{input_folder_path}' have been combined and saved to '{output_file_path}'.")
        except Exception as e:
            print(f"Error while combining or saving the DataFrames: {e}")  # Print error if saving fails
    else:
        print("No valid CSV files found in the specified folder.")

print("Processing complete. All files have been saved. You can now open the CSV file.")
