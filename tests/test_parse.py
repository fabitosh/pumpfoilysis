import polars as pl
from pumpfoilysis.parse import parse_tcx
from pumpfoilysis.schemas import SCHEMA_RAW

def test_parse_tcx():
    """Tests the parse_tcx function."""
    # Given
    file_path = "/Users/fabio/repos/github/fabitosh/pumpfoilysis/tests/cut_activity.tcx"

    # When
    df = parse_tcx(file_path)

    # Then
    assert isinstance(df, pl.DataFrame)
    assert not df.is_empty()
    
    # Infer required columns from SCHEMA_RAW, but rename timestamp to datetime_raw
    expected_columns = list(SCHEMA_RAW.keys())

    # Also check for the other columns that are not in SCHEMA_RAW
    expected_columns.extend(['distance_raw', 'heart_rate_raw', 'speed_raw'])

    assert all(col in df.columns for col in expected_columns)

    # Check dtypes
    assert df['datetime'].dtype == pl.Datetime(time_unit='us', time_zone='UTC')
    assert df['lat_raw'].dtype == pl.Float64
    assert df['lon_raw'].dtype == pl.Float64
    assert df['altitude_raw'].dtype == pl.Float64
    assert df['distance_raw'].dtype == pl.Float64
    assert df['heart_rate_raw'].dtype == pl.Int64
    assert df['speed_raw'].dtype == pl.Float64