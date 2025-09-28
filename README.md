# Pumpfoilysis 🏄‍♂️

Pumpfoilysis is a Python tool designed to analyze GPS activity files of [pumpfoil](https://youtu.be/fyK9_ubjaL4)
activities.
It detects attempted starts, pumping runs, and statistics for each run.
It parses raw sensor data, refines it, and classifies different states of activity.

To my knowledge there is no existing open-source tool, that targets the challenge. Existing closed-source solutions
are either on iOS only, or have not been able to handle the noisy GPS data reliably.

-----

## Core Functionality

The data processing follows a sequential pipeline:

1.  **Parse**: Adapter layer for different file sources (.tcx, .gpx, .fit). Converts to a timeseries dataframe.
2.  **Refine**: Cleans the raw data. Calculates key metrics like velocity, heading, handles gps outliers and gaps.
3.  **Categorize**: Classifies sections.

-----

## Architecture Overview

The project is built with a modular architecture that separates each stage of the data processing pipeline.

The following diagram illustrates the high-level data flow from raw files to classified session data:
![Architecture Diagram](docs/overview.drawio.png)

### Repo Structure

- `docs/`: document design process
- `main.py`: End-to-end workflow.
- `notebooks/`: exploratory non-production code for Development
- `src/`: source code
- `tests/`: collection of recordings and unit tests

## Targets

For MVP v1.0

- [x] Convert `.tcx` files to Polars DataFrame
- [x] GPS Outlier Detection
- [ ] Data Structures for Priors
- [ ] On Foil Detection Algorithm using GPS and Priors
- [ ] Provide Foil Session Summary Statistics
- [ ] Refined Data Export

-----

## Development

### Tech Stack

Each dependency should resolve a clear purpose.

- Language: Python
- Core Data Library: Polars
- Dependency Management: `uv`
- Linting & Formatting: `ruff`
- Testing: `pytest`

### Setup and Usage

First, ensure you have `uv` installed. Then, clone the repository and set up the environment.

1.  **Install dependencies:**
```bash
uv sync --all-extras
```
2.  **Run the main application:**
```bash
uv run main.py
```
3.  **Run tests:**
```bash
uv run pytest
```
4.  **Lint and format code:**
```bash
uv run ruff check .
uv run ruff format .
```
