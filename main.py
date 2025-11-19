from pathlib import Path

from pumpfoilysis.categorize import categorize
from pumpfoilysis.parse import parse_tcx
from pumpfoilysis.refine import calc_refine_features
from pumpfoilysis.summary import calc_session_summary


def main():
    ACTIVITY_PATH = Path("data/activity_20238901238.tcx")
    df_raw = parse_tcx(ACTIVITY_PATH)
    df_refined = calc_refine_features(df_raw)
    df_categorized = categorize(df_refined)
    summary = calc_session_summary(df_categorized)
    print(summary)

if __name__ == "__main__":
    main()
