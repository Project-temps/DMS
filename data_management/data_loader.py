"""Utility functions for loading processed data files."""

import os
import pandas as pd

def load_data(filename='merged_sensor_data.csv', region='Germany'):
    """Load a processed data CSV for the specified region.

    Parameters
    ----------
    filename: str
        Name of the CSV file to load.
    region: str
        Name of the subdirectory under ``data/processed`` containing the file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataframe.
    """

    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', 'processed', region, filename)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        raise FileNotFoundError(f"Data file {data_path} not found.")
