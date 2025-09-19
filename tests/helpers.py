from datetime import datetime
from pathlib import Path

import polars as pl

TESTS_DIR = Path(__file__).resolve().parent


def extract_test_case(
    df: pl.DataFrame,
    name: str,
    start: datetime | None = None,
    end: datetime | None = None,
    csv_dir_path: Path | str = TESTS_DIR,
) -> None:
    """Extracts a test case from the dataframe based on start and end datetime."""
    if start:
        df = df.filter(pl.col("datetime") >= start)
    if end:
        df = df.filter(pl.col("datetime") <= end)
    df.write_csv(Path(csv_dir_path) / f"{name}.csv")


def read_test_case(name: str, csv_dir_path: Path | str = TESTS_DIR) -> pl.DataFrame:
    """Reads a test case from a CSV file."""
    return pl.read_csv(Path(csv_dir_path) / f"{name}.csv", try_parse_dates=True)
