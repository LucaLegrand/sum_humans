import pandas as pd
from datetime import datetime
import re

# Load the CSV file
file_path = r"S:\OneDrive - Fondation EPF\Uni\5eme Année\Project(Σ.humans)\Coding\sum_humans\Data_Extraction and analysis\Data Extraction\detections_full_v3.csv"
data = pd.read_csv(file_path)

# Define the regular expression pattern to match the date-time format in "Image" column
pattern = re.compile(r"^\d{2}_\d{2}_\d{4}_\d{4}")

# Define a function to safely extract the timestamp
def extract_timestamp(image_name):
    # Only parse if the filename matches the expected format
    if pattern.match(image_name):
        date_time_str = image_name.split('_sensor')[0]
        return datetime.strptime(date_time_str, "%d_%m_%Y_%H%M")
    else:
        return None  # Return None for non-matching filenames

# Apply the function to create the Timestamp column
data['Timestamp'] = data['Image'].apply(extract_timestamp)

# Select the relevant columns and drop rows where the timestamp could not be extracted
filtered_data = data[['Timestamp', 'Image', 'Num_people']].dropna()

# Sort the data in descending order by Timestamp
filtered_data = filtered_data.sort_values(by='Timestamp', ascending=True)

# Save the sorted data to a new CSV file
output_path = 'detections_filtered_with_timestamp.csv'  # Set your desired output path
filtered_data.to_csv(output_path, index=False)

print(f"Filtered and sorted data saved to {output_path}")
