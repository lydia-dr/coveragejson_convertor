"""
Module: parser.py
Description: Reads weather CSV files and converts rows into WeatherObservation objects.
"""

import pandas as pd
from dateutil.parser import parse
from .models import WeatherObservation

def load_weather_csv(file_path: str) -> list[WeatherObservation]:
    """
    Load weather observations from a CSV file.

    Expected CSV columns:
      - time
      - longitude
      - latitude
      - temperature
    Returns a list of WeatherObservation objects.
    """
    # Load CSV
    df = pd.read_csv(file_path)

    # Basic validation
    required_cols = {"time", "longitude", "latitude", "temperature"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    # Initialise list of observations
    observations = []

    # Convert each row of the CSV into a WeatherObservation object and collect them in a list
    for _, row in df.iterrows():
        obs = WeatherObservation(
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            timestamp=parse(row["time"]),
            temperature=float(row["temperature"])
        )
        observations.append(obs)

    return observations