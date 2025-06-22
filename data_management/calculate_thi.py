"""Calculate Temperature-Humidity Index (THI) from processed data."""

import pandas as pd
import os

def calculate_thi():
    # Define the base directory and file paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    germany_file = os.path.join(base_dir, 'data', 'processed', 'Germany', 'hourly_merged_sensor_data.csv')  # Adjust the filename
    poland_file = os.path.join(base_dir, 'data', 'processed', 'Poland', 'hourly_merged_sensor_data.csv')  # Adjust the filename

    # Load the data
    germany_data = pd.read_csv(germany_file)
    poland_data = pd.read_csv(poland_file)

    # Assuming the columns for temperature and humidity are named 'Temperature' and 'Humidity'
    # You may need to adjust these names based on your actual CSV structure
    germany_thi_data = []
    poland_thi_data = []
    
    for index, row in germany_data.iterrows():
        temperature = row['temperature']
        humidity = row['humidity']
        thi = (1.8 * temperature + 32) - ((0.55 - 0.0055 * humidity) * (1.8 * temperature - 26))
        germany_thi_data.append({'Timestamp': row['datetime'], 'THI': thi})

    for index, row in poland_data.iterrows():
        temperature = row['temperature']
        humidity = row['humidity']
        thi = (1.8 * temperature + 32) - ((0.55 - 0.0055 * humidity) * (1.8 * temperature - 26))
        poland_thi_data.append({'Timestamp': row['datetime'], 'THI': thi})

    return pd.DataFrame(germany_thi_data), pd.DataFrame(poland_thi_data)

# You can now test your API by sending a GET request to /api/calculate_thi/. This will return the THI data in JSON format.

