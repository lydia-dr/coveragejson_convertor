# CoverageJSON Converter

## Overview
`coveragejson_converter` is a Python tool to convert weather observation CSV files into valid [CoverageJSON](https://covjson.org/) documents.
It is designed to handle **time series data for a single geographic point**, including temperature measurements in Kelvin, and produces a self-describing JSON file suitable for analysis or visualization.

This project is intended to be shared as a self-contained folder. The instructions below ensure it can be set up reproducibly on the recipient’s machine.

---

## Requirements
- **Python 3.11** (required to match versions in `requirements.txt`)
- [Conda](https://docs.conda.io/en/latest/miniconda.html) is recommended for environment management

---

## Features
- Parse CSV files containing timestamped weather data
- Represent each observation as a `WeatherObservation` domain object
- Convert observations into CoverageJSON format with correct axes (`t`, `x`, `y`) and `air_temperature` parameter metadata
- Command-line interface (CLI) for easy conversion
- Logging for runtime feedback and error reporting
- Fully tested with unit tests for parser and transformer modules

---

## Project Structure

```
coveragejson_converter/
│
├── src/
│   └── coveragejson_converter/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── parser.py
│       └── transformer.py
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   └── test_transformer.py
├── data/
│   └── input_data.csv
├── output/
│   └── coverage.json
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation with Conda

1. Create a new Conda environment with Python 3.11:

```bash
conda create -n coverage_json python=3.11 -y
conda activate coverage_json
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

> **Note:** Using Python 3.11 ensures the versions in `requirements.txt` install correctly.

---

## Usage

Convert a CSV file to CoverageJSON via the CLI:

```bash
PYTHONPATH=src python -m coveragejson_converter.main \
    --input data/input_data.csv \
    --output output/coverage.json
```

### Arguments

| Flag | Description |
|------|-------------|
| `--input`, `-i` | Path to the input CSV file containing weather observations |
| `--output`, `-o` | Path to write the CoverageJSON output |

---

## Testing

Run all tests with `pytest`:

```bash
PYTHONPATH=src python -m pytest
```

Tests cover:

- CSV parsing
- Domain object creation
- CoverageJSON transformation
- Error handling for empty or invalid input

---

## Design Decisions and Assumptions

- **Domain Model:** `WeatherObservation` represents a single observation with timestamp, latitude, longitude, and temperature
- **Single-point assumption:** Designed for one geographic location with multiple timestamps, per project requirements
- **Timezone handling:** All timestamps are parsed with UTC awareness
- **Logging:** `main.py` uses `logging` to provide runtime feedback and error reporting

---

## Possible Future Improvements

- Support multiple geographic points (lat/lon grids)
- Support altitude measurements
- Support additonal weather parameters (e.g., humidity, wind speed)
- Validate CoverageJSON against official schema
- Stream large CSV files efficiently

---

## Example Output

```JSON
{
  "type": "Coverage",
  "domain": {
    "type": "Domain",
    "domainType": "PointSeries",
    "axes": {
      "t": {
        "values": [
          "2026-02-16T00:00:00+00:00",
          "2026-02-16T01:00:00+00:00",
          "2026-02-16T02:00:00+00:00"
        ]
      },
      "x": {
        "values": [-3.48]
      },
      "y": {
        "values": [50.73]
      }
    },
    "referencing": [
      {
        "coordinates": ["y", "x"],
        "system": {
          "type": "GeographicCRS",
          "id": "http://www.opengis.net/def/crs/EPSG/0/4326"
        }
      },
      {
        "coordinates": ["t"],
        "system": {
          "type": "TemporalRS",
          "calendar": "Gregorian"
        }
      }
    ]
  },
  "parameters": {
    "air_temperature": {
      "type": "Parameter",
      "description": { "en": "Air temperature" },
      "unit": {
        "label": { "en": "Kelvin" },
        "symbol": { "value": "K", "type": "http://www.opengis.net/def/uom/UCUM/" }
      },
      "observedProperty": {
        "id": "http://vocab.nerc.ac.uk/standard_name/air_temperature/",
        "label": { "en": "Air Temperature" }
      }
    }
  },
  "ranges": {
    "air_temperature": {
      "type": "NdArray",
      "dataType": "float",
      "axisNames": ["t", "y", "x"],
      "shape": [3, 1, 1],
      "values": [275.2, 275.5, 275.7]
    }
  }
}
```

