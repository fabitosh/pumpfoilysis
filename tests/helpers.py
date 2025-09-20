from datetime import datetime, timezone
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
        start = _ensure_tz_aware(start)
        df = df.filter(pl.col("datetime") >= start)
    if end:
        end = _ensure_tz_aware(end)
        df = df.filter(pl.col("datetime") <= end)
    df.write_csv(Path(csv_dir_path) / f"{name}.csv")


def _ensure_tz_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def read_test_case(name: str, csv_dir_path: Path | str = TESTS_DIR) -> pl.DataFrame:
    """Reads a test case from a CSV file."""
    return pl.read_csv(Path(csv_dir_path) / f"{name}.csv", try_parse_dates=True)
