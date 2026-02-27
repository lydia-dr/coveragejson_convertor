"""
Test suite for the parser module of coveragejson_converter.

Verifies that:
- CSV files are correctly parsed into WeatherObservation objects.
- Missing required columns raise a ValueError.
- Timestamps are correctly parsed as UTC-aware datetimes.
"""

import pytest
from datetime import datetime
from dateutil.tz import tzutc
from src.coveragejson_converter.parser import load_weather_csv
from src.coveragejson_converter.models import WeatherObservation
from pathlib import Path

# Sample CSV data matching the provided input
CSV_DATA = """time,longitude,latitude,temperature
2026-02-16T00:00Z,-3.48,50.73,275.2
2026-02-16T01:00Z,-3.48,50.73,275.5
2026-02-16T02:00Z,-3.48,50.73,275.7
"""

def test_load_weather_csv(tmp_path):
    # Create a temporary CSV file
    csv_file = tmp_path / "input_data.csv"
    csv_file.write_text(CSV_DATA)

    # Load observations
    observations = load_weather_csv(str(csv_file))

    # Assertions
    assert len(observations) == 3
    assert all(isinstance(obs, WeatherObservation) for obs in observations)

    # Check first observation values
    first_obs = observations[0]
    assert first_obs.latitude == 50.73
    assert first_obs.longitude == -3.48
    # UTC-aware datetime assertion
    expected_ts = datetime(2026, 2, 16, 0, 0, tzinfo=tzutc())
    assert first_obs.timestamp == expected_ts
    assert first_obs.temperature == 275.2

def test_missing_columns(tmp_path):
    # CSV missing the 'time' column
    bad_csv = """longitude,latitude,temperature
-3.48,50.73,275.2
"""
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text(bad_csv)

    with pytest.raises(ValueError, match="CSV must contain columns"):
        load_weather_csv(str(csv_file))