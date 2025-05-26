import os
import pandas as pd

def load_data(filename='merged_sensor_data.csv'):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', 'processed', 'germany', filename)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        raise FileNotFoundError(f"Data file {data_path} not found.")
