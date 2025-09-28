from pumpfoilysis.categorize import calc_rolling_metrics
from pumpfoilysis.refine import calc_refine_features
from tests.helpers import read_test_sample


def test_calc_rolling_metrics_does_not_fill_gps_nulls():
    """polars rolling mean does fill up null values."""
    df = read_test_sample("consecutive_gps_gaps.csv")
    df_refined = calc_refine_features(df)
    # The first row will have a null velocity as there is not yet a delta between two measurement points
    df_out = calc_rolling_metrics(df_refined, window_size="3s")[1:]
    assert df_out[1:].get_column("lat_raw").null_count() == df_out.get_column("velocity_smoothed").null_count()
