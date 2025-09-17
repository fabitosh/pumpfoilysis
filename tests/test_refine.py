
import polars as pl
import polars.testing

from pumpfoilysis.refine import linearize_geo
def test_linearize_switzerland():
    ref_lat, ref_lon = 47.384827, 8.5362690
    df = pl.DataFrame({
        'lat_raw': [ref_lat, 47.384],
        'lon_raw': [ref_lon, 8.5362]
    })
    linearized_df = linearize_geo(df, (ref_lat, ref_lon))
    assert 'x' in linearized_df.columns
    assert 'y' in linearized_df.columns
    expected_x = pl.Series("x", [0.0, -5.1948])
    expected_y = pl.Series("y", [0.0, -91.958])
    pl.testing.assert_series_equal(linearized_df['x'], expected_x, abs_tol=0.01)
    pl.testing.assert_series_equal(linearized_df['y'], expected_y, abs_tol=0.01)


def test_linearize_equator():
    ref_lat, ref_lon = 0.384827, 8.5362690
    df = pl.DataFrame({
        'lat_raw': [ref_lat, 0.384],
        'lon_raw': [ref_lon, 8.5362]
    })
    linearized_df = linearize_geo(df, (ref_lat, ref_lon))
    assert 'x' in linearized_df.columns
    assert 'y' in linearized_df.columns
    expected_x = pl.Series("x", [0.0, -7.6723])
    expected_y = pl.Series("y", [0.0, -91.958])
    pl.testing.assert_series_equal(linearized_df['x'], expected_x, abs_tol=0.01)
    pl.testing.assert_series_equal(linearized_df['y'], expected_y, abs_tol=0.01)
