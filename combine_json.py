import json
import os

# List of JSON files to merge
json_files = ['wp-json-data/data1.json', 'wp-json-data/data2.json', 'wp-json-data/data3.json']
combined_data = []

# Load and combine data from each file
for file_name in json_files:
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)  # Parse the JSON content in python dictionary
            combined_data.append(data)  # Append the data to the list
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {file_name}.")