"""
Module: transformer.py
Description:
Transforms WeatherObservation domain objects into a valid
CoverageJSON structure representing a time series at a single
geographic point (PointSeries).

The transformer converts parsed observations into:

- domain      → spatial + temporal axes definition
- parameters  → metadata describing the measured variable
- ranges      → flattened measurement values array

CoverageJSON Specification:
https://covjson.org/
"""

from typing import List, Dict
from .models import WeatherObservation


def build_coveragejson(observations: List[WeatherObservation]) -> Dict:
    """
    Convert WeatherObservation objects into a CoverageJSON document.

    Args:
        observations (List[WeatherObservation]):
            Parsed weather observations.

    Returns:
        Dict: CoverageJSON object.
    """

    if not observations:
        raise ValueError("No observations provided")

    # ---------------------------------------------------------
    # 1. Extract axes
    # ---------------------------------------------------------
    # CoverageJSON separates coordinates (domain) from data values (ranges).

    times = sorted(obs.timestamp.isoformat() for obs in observations)
    longitudes = sorted({obs.longitude for obs in observations})
    latitudes = sorted({obs.latitude for obs in observations})

    # Expected for this exercise:
    # - single latitude
    # - single longitude
    # - multiple timestamps

    # ---------------------------------------------------------
    # 2. Build flattened values array
    # ---------------------------------------------------------
    # CoverageJSON requires values ordered according to axisNames.
    # axisNames = ["t", "y", "x"]

    values = []

    for t in times:
        for y in latitudes:
            for x in longitudes:
                match = next(
                    (
                        obs for obs in observations
                        if obs.timestamp.isoformat() == t
                        and obs.latitude == y
                        and obs.longitude == x
                    ),
                    None,
                )

                values.append(
                    match.temperature if match else None
                )

    # ---------------------------------------------------------
    # 3. Assemble CoverageJSON structure
    # ---------------------------------------------------------

    coveragejson = {
        "type": "Coverage",

        # ---------------- DOMAIN ----------------
        "domain": {
            "type": "Domain",
            "domainType": "PointSeries",

            "axes": {
                "t": {"values": times},
                "x": {"values": longitudes},
                "y": {"values": latitudes},
            },

            # OGC referencing information
            "referencing": [
                {
                    "coordinates": ["y", "x"],
                    "system": {
                        "type": "GeographicCRS",
                        "id": "http://www.opengis.net/def/crs/EPSG/0/4326",
                    },
                },
                {
                    "coordinates": ["t"],
                    "system": {
                        "type": "TemporalRS",
                        "calendar": "Gregorian",
                    },
                },
            ],
        },

        # ---------------- PARAMETERS ----------------
        "parameters": {
            "air_temperature": {
                "type": "Parameter",
                "description": {
                    "en": "Air temperature"
                },
                "unit": {
                    "label": {"en": "Kelvin"},
                    "symbol": {
                        "value": "K",
                        "type": "http://www.opengis.net/def/uom/UCUM/",
                    },
                },
                "observedProperty": {
                    "id": "http://vocab.nerc.ac.uk/standard_name/air_temperature/",
                    "label": {"en": "Air Temperature"},
                },
            }
        },

        # ---------------- RANGES ----------------
        "ranges": {
            "air_temperature": {
                "type": "NdArray",
                "dataType": "float",
                "axisNames": ["t", "y", "x"],
                "shape": [
                    len(times),
                    len(latitudes),
                    len(longitudes),
                ],
                "values": values,
            }
        },
    }

    return coveragejson