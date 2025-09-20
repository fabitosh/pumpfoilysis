import polars as pl
import polars.testing
import pytest

from tests.helpers import read_test_sample
from pumpfoilysis.refine import _linearize_geo, calc_refine_features, _calc_gps_features


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
