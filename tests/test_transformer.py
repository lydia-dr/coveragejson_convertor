"""
Tests for transformer module.

Validates conversion of WeatherObservation objects
into a CoverageJSON structure.
"""

from datetime import datetime
from dateutil.tz import tzutc

from coveragejson_converter.models import WeatherObservation
from coveragejson_converter.transformer import build_coveragejson


def sample_observations():
    """Create sample WeatherObservation objects for testing."""
    return [
        WeatherObservation(
            timestamp=datetime(2026, 2, 16, 0, 0, tzinfo=tzutc()),
            latitude=50.73,
            longitude=-3.48,
            temperature=275.2,
        ),
        WeatherObservation(
            timestamp=datetime(2026, 2, 16, 1, 0, tzinfo=tzutc()),
            latitude=50.73,
            longitude=-3.48,
            temperature=275.5,
        ),
        WeatherObservation(
            timestamp=datetime(2026, 2, 16, 2, 0, tzinfo=tzutc()),
            latitude=50.73,
            longitude=-3.48,
            temperature=275.7,
        ),
    ]


# --------------------------------------------------------------------------------
# Test: Verify top-level CoverageJSON structure
# --------------------------------------------------------------------------------
def test_build_coveragejson_structure():
    """
    Ensure that the CoverageJSON returned by the transformer has all required
    top-level keys: 'type', 'domain', 'parameters', and 'ranges'.
    """
    covjson = build_coveragejson(sample_observations())
    assert covjson["type"] == "Coverage"
    assert "domain" in covjson
    assert "parameters" in covjson
    assert "ranges" in covjson


# --------------------------------------------------------------------------------
# Test: Validate the domain axes
# --------------------------------------------------------------------------------
def test_domain_axes():
    """
    Check that the 'domain' axes are correctly built from the observations:
    - 'x' corresponds to longitude
    - 'y' corresponds to latitude
    - 't' corresponds to time
    """
    covjson = build_coveragejson(sample_observations())
    axes = covjson["domain"]["axes"]
    assert axes["x"]["values"] == [-3.48]
    assert axes["y"]["values"] == [50.73]
    assert len(axes["t"]["values"]) == 3


# --------------------------------------------------------------------------------
# Test: Verify parameter metadata
# --------------------------------------------------------------------------------
def test_parameter_metadata():
    """
    Ensure that the 'air_temperature' parameter exists and includes:
    - type: Parameter
    - observedProperty linking to the NERC standard_name vocabulary
    """
    covjson = build_coveragejson(sample_observations())
    param = covjson["parameters"]["air_temperature"]
    assert param["type"] == "Parameter"
    assert param["observedProperty"]["id"].endswith("air_temperature/")


# --------------------------------------------------------------------------------
# Test: Check that temperature values are ordered correctly
# --------------------------------------------------------------------------------
def test_range_values_order():
    """
    Confirm that the 'values' array in the NdArray matches the temporal order
    of observations (time increasing). This ensures scientific correctness.
    """
    covjson = build_coveragejson(sample_observations())
    values = covjson["ranges"]["air_temperature"]["values"]
    assert values == [275.2, 275.5, 275.7]


# --------------------------------------------------------------------------------
# Test: Validate NdArray shape
# --------------------------------------------------------------------------------
def test_shape_definition():
    """
    Ensure the NdArray 'shape' matches the dimensions of the domain axes:
    - Time length = 3
    - Latitude length = 1
    - Longitude length = 1
    """
    covjson = build_coveragejson(sample_observations())
    shape = covjson["ranges"]["air_temperature"]["shape"]
    assert shape == [3, 1, 1]


# --------------------------------------------------------------------------------
# Test: Handle empty observation list gracefully
# --------------------------------------------------------------------------------
def test_empty_observations_error():
    """
    The transformer should raise a ValueError if provided with an empty
    list of WeatherObservation objects. This tests defensive programming.
    """
    import pytest

    with pytest.raises(ValueError):
        build_coveragejson([])