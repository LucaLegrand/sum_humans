import requests
import csv

# List of sensor IDs
sensor_ids = [32, 33]

# Sensor names corresponding to IDs
sensor_names = {
    32: "sound",
    33: "Co2",
}

# Base URL for the API
base_url = "http://192.168.139.27/measure.php"

# Number of rows to retrieve (or fetch all available data if API allows)
row_count = 120000 # Row Count

# Dictionary to hold data for each sensor
sensor_data = {
    32: [],  # For sound sensor
    33: []   # For CO2 sensor
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

# Write the data to a CSV file
with open("sensor_data.csv", mode='w', newline='') as csv_file:
    fieldnames = ["time", "sound_value", "co2_value"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Assuming both sensors have the same number of records, iterate over them
    for i in range(min(len(sensor_data[32]), len(sensor_data[33]))):
        writer.writerow({
            "time": sensor_data[32][i]["time"], 
            "sound_value": sensor_data[32][i]["value"],
            "co2_value": sensor_data[33][i]["value"]
        })

print("CSV file 'sensor_data.csv' created successfully.")
