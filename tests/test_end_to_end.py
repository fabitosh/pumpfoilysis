from pumpfoilysis.refine import calc_refine_features
from tests.helpers import read_test_sample

def test_first_run()
    df_raw = read_test_sample("ermitage_first_run_gps_jiggle_in_water")
    df_refined = calc_refine_features(df_raw)
    df_classified =


