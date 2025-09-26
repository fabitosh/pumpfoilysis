from datetime import datetime

import polars as pl
import polars.testing
import pytest

from pumpfoilysis.refine import _linearize_geo, _calc_gps_features, calc_refine_features
from tests.helpers import read_test_sample


def test_linearize_switzerland():
    ref_lat, ref_lon = 47.384827, 8.5362690
    df = pl.DataFrame({"lat_raw": [ref_lat, 47.384], "lon_raw": [ref_lon, 8.5362]})
    linearized_df = _linearize_geo(df, (ref_lat, ref_lon))
    assert "x" in linearized_df.columns
    assert "y" in linearized_df.columns
    expected_x = pl.Series("x", [0.0, -5.1948])
    expected_y = pl.Series("y", [0.0, -91.958])
    pl.testing.assert_series_equal(linearized_df["x"], expected_x, abs_tol=0.01)
    pl.testing.assert_series_equal(linearized_df["y"], expected_y, abs_tol=0.01)


def test_linearize_equator():
    ref_lat, ref_lon = 0.384827, 8.5362690
    df = pl.DataFrame({"lat_raw": [ref_lat, 0.384], "lon_raw": [ref_lon, 8.5362]})
    linearized_df = _linearize_geo(df, (ref_lat, ref_lon))
    assert "x" in linearized_df.columns
    assert "y" in linearized_df.columns
    expected_x = pl.Series("x", [0.0, -7.6723])
    expected_y = pl.Series("y", [0.0, -91.958])
    pl.testing.assert_series_equal(linearized_df["x"], expected_x, abs_tol=0.01)
    pl.testing.assert_series_equal(linearized_df["y"], expected_y, abs_tol=0.01)


def test_linearize_no_ref_coords_takes_min():
    df = pl.DataFrame({"lat_raw": [47.384827, 47.384], "lon_raw": [8.5362690, 8.5362]})
    linearized_df = _linearize_geo(df, linearization_coordinate=None)
    expected_x = pl.Series("x", [5.1948, 0.0])
    expected_y = pl.Series("y", [91.958, 0.0])
    pl.testing.assert_series_equal(linearized_df["x"], expected_x, abs_tol=0.01)
    pl.testing.assert_series_equal(linearized_df["y"], expected_y, abs_tol=0.01)


def test_calc_gps_features_raises_if_gps_nans():
    df = read_test_sample("consecutive_gps_gaps.csv")
    # there are nan values for lat, lon in multiple rows.
    with pytest.raises(RuntimeError, match="contains null values for lat_raw and lon_raw"):
        _ = _calc_gps_features(df)


def test_calc_refine_features_handles_gps_gaps():
    """The raw file has two short gaps. 1 sample off, 1 on, 2 off, rest on.
    We want to make sure that the average speed calculation takes the additional time into account."""
    df = read_test_sample("consecutive_gps_gaps.csv")
    df_gps = _calc_gps_features(df.filter(pl.col("lat_raw").is_not_null()).select(["datetime", "lat_raw", "lon_raw"]))
    pl.testing.assert_series_equal(df_gps.get_column('velocity_kmh'),
                                   pl.Series('velocity_kmh', [
                                       None,
                                       11.860085,
                                       11.712399,
                                       11.210484,
                                       10.846201,
                                   ]),
                                   abs_tol=0.01)


def test_calc_refine_features():
    df = read_test_sample("consecutive_gps_gaps.csv")
    df_out = calc_refine_features(df)
    assert df_out.shape[0] == df.shape[0]
    v = df_out.get_column("velocity_kmh").is_not_null()
    assert v.sum() == 4 # First sample has no delta. Remainder should be data gaps

def test_polars_rolling():
    """Get clarity on how polars rolling functions behave.
    The window is only backwards looking.
    One null in the window -> take the remaining values."""
    n = 5
    df = pl.DataFrame({
    "datetime": pl.datetime_range(
        start=datetime(2025, 9, 26, 15, 0),
        end=datetime(2025, 9, 27, 0, 0),
        interval="1h",
        eager=True,
    ).slice(0, n),
    "value": pl.arange(1, n + 1, eager=True).replace(3, None).replace(4, None),
    })
    out = df.rolling(index_column="datetime", period="2h").agg([
        pl.mean("value").alias("mean_value"),
    ])
    expected = pl.DataFrame({
        "datetime": df.get_column("datetime"),
        "mean_value": pl.Series("mean_value", [1.0, 1.5, 2.0, None, 5.0]),
    })
    pl.testing.assert_frame_equal(out, expected, abs_tol=0.01)
