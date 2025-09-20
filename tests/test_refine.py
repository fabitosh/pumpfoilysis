import polars as pl
import polars.testing

from helpers import read_test_sample
from pumpfoilysis.refine import _linearize_geo, calc_refine_features


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

def test_calc_refine_features_handles_gps_gaps():
    df = read_test_sample("samples/consecutive_gps_gaps.csv")
    df = calc_refine_features(df)
    assert "gps_sampling_rate" in df.columns