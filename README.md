# Project: CoverageJSON Converter

## Project Overview
This project reads meteorological CSV data and generates a CoverageJSON file
in accordance with the CoverageJSON standard (https://covjson.org/). 
It is designed as a modular Python backend service.

## Project Structure
- `src/coveragejson_converter/` - main source code
- `tests/` - unit tests for modules
- `data/` - example CSV data files
- `output/` - generated CoverageJSON files

## Implementation Plan
1. **Main Entry Point:** `main.py` to run the pipeline
2. **Modules:**  
   - `parser.py` – load and validate CSV data  
   - `models.py` – define domain objects  
   - `transformer.py` – prepare axes and values for CoverageJSON  
   - `coveragejson.py` – assemble CoverageJSON structure
3. **Tests:** Unit tests for parsing, transformation, and CoverageJSON output
4. **Output:** CoverageJSON saved to `output/coverage.json`

## How to Run
```bash
python src/coveragejson_converter/main.py data/weather.csv