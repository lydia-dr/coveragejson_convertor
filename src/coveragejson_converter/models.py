"""
Module: models.py
Description: Defines domain models for the CoverageJSON converter.
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherObservation:
    """
    Represents a single weather observation at a specific location and time.

    Attributes:
        timestamp (datetime): The time of the observation.
        latitude (float): Latitude in decimal degrees (EPSG:4326).
        longitude (float): Longitude in decimal degrees (EPSG:4326).
        temperature (float): Temperature measurement (Kelvin).
    """
    timestamp: datetime
    latitude: float
    longitude: float
    temperature: float