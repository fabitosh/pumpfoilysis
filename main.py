from pathlib import Path

from pumpfoilysis.parse import parse_tcx
from pumpfoilysis.refine import calc_refine_features


def main():
    ACTIVITY_PATH = Path("data/activity_20238901238.tcx")
    df_raw = parse_tcx(ACTIVITY_PATH)
    df_refined = calc_refine_features(df_raw)


if __name__ == "__main__":
    main()
