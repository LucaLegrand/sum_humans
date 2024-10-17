import requests
import json

# List of sensor IDs
sensor_ids = [32, 19, 33, 40, 43, 46, 227]

# Base URL for the API
base_url = "https://preprodapi.mde.epf.fr/measure.php"

# Dictionary to store the results for JavaScript output
sensor_data = {}

# Sensor names
sensor_names = {
    32: "sound",      
    19: "Co2 1",      
    33: "Co2 2",
    40: "Co2 3",
    43: "Co2 4",
    46: "Co2 5",
    227: "Co2 6"
}

# Loop through each sensor ID and get the final reading
for sensor_id in sensor_ids:
    # Set the parameters to get the latest reading for each sensor
    params = {
        'id': sensor_id,
        'row_count': 1  # Fetch the most recent reading
    }
    
    # Make the request to the API
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract the sensor ID, the latest value, and the sensor name
        sensor_data[sensor_id] = {
            "sensor": sensor_names[sensor_id],  # Add the corresponding sensor name
            "id_system_sensor": data[0]["general"]["id_system_sensor"],
            "value": data[1]["value"]
        }
    else:
        print(f"Failed to retrieve data for Sensor ID {sensor_id}")

# Create JavaScript file content
js_content = "// Sensor Data\nvar sensorData = [\n"
for sensor in sensor_data.values():
    js_content += f'  {{\n'
    js_content += f'    "sensor": "{sensor["sensor"]}",\n'
    js_content += f'    "id_system_sensor": "{sensor["id_system_sensor"]}",\n'
    js_content += f'    "value": "{sensor["value"]}"\n'
    js_content += f'  }},\n'
js_content = js_content.rstrip(",\n") + "\n];"  # Remove the last comma and close the array

# Write the content to a JavaScript file
with open("sensorData.js", "w") as js_file:
    js_file.write(js_content)

print("JavaScript file 'sensorData.js' created successfully.")
