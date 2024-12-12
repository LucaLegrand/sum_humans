import requests
import csv
import pandas as pd
from datetime import datetime, timedelta

# List of sensor IDs
sensor_ids = [33, 32, 213]  # CO2 (33), Sound (32), Ventilation (213)

# Sensor names corresponding to IDs
sensor_names = {
    33: "co2",        # CO2 sensor
    32: "sound",      # Sound sensor
    213: "ventilation"  # Ventilation sensor
}

# Base URL for the API
base_url = "https://preprodapi.mde.epf.fr/measure.php"

# Number of rows to retrieve (or fetch all available data if API allows)
row_count = 120000  # Row Count

# Dictionary to hold data for each sensor
sensor_data = {
    33: [],  # For CO2 sensor
    32: [],  # For Sound sensor
    213: []  # For Ventilation sensor
}

# Loop through each sensor and fetch the data
for sensor_id in sensor_ids:
    # Set parameters to fetch all the data for each sensor
    params = {
        'id': sensor_id,
        'row_count': row_count  # Specify the number of records to fetch
    }

    # Make the request to the API
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Adjust extraction based on actual response format
        for entry in data:
            if "created" in entry and "value" in entry:
                sensor_data[sensor_id].append({
                    "time": entry["created"],  # Timestamp of the reading
                    "value": entry["value"]    # Sensor value
                })
            else:
                print(f"Skipping entry without 'created' or 'value': {entry}")
    else:
        print(f"Failed to retrieve data for Sensor ID {sensor_id}")

# Combine the sensor data into a single list of rows
combined_data = []
for i in range(min(len(sensor_data[33]), len(sensor_data[32]), len(sensor_data[213]))):
    combined_data.append({
        "time": sensor_data[33][i]["time"],  # Assuming all sensors have the same time
        "co2_value": sensor_data[33][i]["value"],
        "sound_value": sensor_data[32][i]["value"],
        "ventilation_value": sensor_data[213][i]["value"]
    })

# Now, load the combined data into a pandas DataFrame
df = pd.DataFrame(combined_data)

# Convert 'time' column to datetime
df['time'] = pd.to_datetime(df['time'])

# Date when the rounding rule changed
change_date = datetime(2023, 6, 19, 13, 14, 27)

# Function to round timestamps based on the change date
def round_time(row):
    if row['time'] < change_date:
        # Round to nearest 5 minutes
        delta = row['time'].minute % 5
        rounded_time = row['time'] - timedelta(minutes=delta)
    else:
        # Round to nearest 10 minutes
        delta = row['time'].minute % 10
        rounded_time = row['time'] - timedelta(minutes=delta)
        
    return rounded_time.replace(second=0, microsecond=0)

# Apply the rounding function to the 'time' column
df['rounded_time'] = df.apply(round_time, axis=1)

# Get today's date in DD_MM_YYYY format
today_date = datetime.now().strftime("%d_%m_%Y")

# Create the filename dynamically
filename = f"all_sensor_data_{today_date}.csv"

# Write the data to a CSV file
df[['rounded_time', 'co2_value', 'sound_value', 'ventilation_value']].to_csv(filename, index=False)

print(f"CSV file '{filename}' created successfully.")
