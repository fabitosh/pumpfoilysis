import polars as pl
from pumpfoilysis.parse import parse_tcx
from pumpfoilysis.schemas import SCHEMA_RAW


def test_parse_tcx():
    file_path = "tests/samples/cut_activity.tcx"
    df = parse_tcx(file_path)
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()

    # Minimum Set defined in Schema that will be used subsequently
    expected_columns = list(SCHEMA_RAW.keys())
    # Optional columns that are present in Forerunner 945 LTE recordings
    expected_columns.extend(["distance_raw", "heart_rate_raw", "speed_raw"])
    assert all(col in df.columns for col in expected_columns)

    assert df["datetime"].dtype == pl.Datetime(time_unit="us", time_zone="UTC")
    assert df["lat_raw"].dtype == pl.Float64
    assert df["lon_raw"].dtype == pl.Float64
    assert df["altitude_raw"].dtype == pl.Float64
    assert df["distance_raw"].dtype == pl.Float64
    assert df["heart_rate_raw"].dtype == pl.Int64
    assert df["speed_raw"].dtype == pl.Float64
