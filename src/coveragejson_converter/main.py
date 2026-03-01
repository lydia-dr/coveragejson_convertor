"""
Main entry point for the CoverageJSON converter.

Reads a CSV file of weather observations and outputs a valid CoverageJSON document.
"""

import argparse
import json
import logging
from pathlib import Path

from coveragejson_converter.parser import load_weather_csv
from coveragejson_converter.transformer import build_coveragejson

# --------------------------------------------------------------------------------
# Configure logging
# --------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------
# Main pipeline function
# --------------------------------------------------------------------------------
def main(input_csv: str, output_json: str):
    """
    Full pipeline: CSV → WeatherObservation → CoverageJSON → JSON file.
    
    Args:
        input_csv (str): Path to input CSV file with weather observations.
        output_json (str): Path to write CoverageJSON output.
    """
    input_path = Path(input_csv)
    output_path = Path(output_json)

    # Step 1: Validate input CSV exists
    if not input_path.is_file():
        logger.error(f"Input CSV not found: {input_path}")
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    # Step 2: Load observations
    try:
        observations = load_weather_csv(str(input_path))
        if not observations:
            logger.warning("No observations found in CSV.")
    except Exception as e:
        logger.error(f"Failed to load CSV: {e}")
        raise

    logger.info(f"Loaded {len(observations)} observations from CSV.")

    # Step 3: Build CoverageJSON
    try:
        covjson = build_coveragejson(observations)
    except Exception as e:
        logger.error(f"Failed to build CoverageJSON: {e}")
        raise

    # Step 4: Write CoverageJSON to file
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(covjson, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to write CoverageJSON: {e}")
        raise

    logger.info(f"CoverageJSON written to {output_path}")


# --------------------------------------------------------------------------------
# Command-line interface
# --------------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert weather CSV into CoverageJSON."
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input CSV file containing weather observations."
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to output CoverageJSON file."
    )
    return parser.parse_args()


# --------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_args()
    main(args.input, args.output)