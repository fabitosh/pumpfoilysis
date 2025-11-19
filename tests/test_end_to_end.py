from pumpfoilysis.categorize import categorize
from pumpfoilysis.refine import calc_refine_features
from pumpfoilysis.summary import calc_session_summary
from tests.helpers import read_test_sample


def test_pipeline():
    df_raw = read_test_sample("ermitage_first_run_gps_jiggle_in_water.csv")
    assert not df_raw.is_empty()
    assert "datetime" in df_raw.columns

    df_refined = calc_refine_features(df_raw)
    assert "velocity_kmh" in df_refined.columns
    assert "heading" in df_refined.columns

    df_categorized = categorize(df_refined)
    assert "is_pumping" in df_categorized.columns

    summary = calc_session_summary(df_categorized)
    assert "run_id" in summary.columns
    assert "distance_m" in summary.columns

    # Check if we found any runs
    if not summary.is_empty():
        assert summary["distance_m"].sum() > 0
