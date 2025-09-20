import math

import polars as pl

# For now, we define the parameters in a hacky fashion here.

# Foil Params
SPEED_PUMP_MAX_KMH = 22.0  # Takoon Pump 1700
# for short durations, extremely slow speeds are realistic but cannot be sustained.
SPEED_PUMP_MIN_KMH = 5.0  # Stall Speed

# Off-Foil Params
SPEED_SWIM_MAX_KMH = 3.0
SPEED_WALK_MAX_KMH = 7.0
MAX_OFF_FOIL_SPEED_KMH = max(SPEED_SWIM_MAX_KMH, SPEED_WALK_MAX_KMH)

SPEED_OUTLIER_KMH = 2 * SPEED_PUMP_MAX_KMH


def calc_refine_features(df: pl.DataFrame) -> pl.DataFrame:
    cols_index = ["datetime"]
    cols_gps = ["lat_raw", "lon_raw"]
    df_idx = _calc_generic_features(df.drop(cols_gps))
    df_gps = _filter_null_gps(df).select(cols_index + cols_gps)
    return df_idx.join(_calc_gps_features(df_gps), on=cols_index, how="left")


def _calc_generic_features(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        sampling_rate=pl.col("datetime").diff(),
        # delta_distance_raw=pl.col("distance_raw").diff(),  # can be used as comparison with own calculations
    )


def _calc_gps_features(df: pl.DataFrame, min_outlier_kmh: float = SPEED_OUTLIER_KMH) -> pl.DataFrame:
    """Expects a dataframe with nan-filtered gps values."""
    if df.get_column("lat_raw").has_nulls() or df.get_column("lon_raw").has_nulls():
        raise RuntimeError(
            "DataFrame contains null values for lat_raw and lon_raw. \n"
            "Please filter out rows with missing GPS data before calling this function."
        )
    df = _linearize_geo(df)
    return (
        df.with_columns(
            gps_sampling_rate=pl.col("datetime").diff(),
            delta_x=pl.col("x").diff(),
            delta_y=pl.col("y").diff(),
        )
        .with_columns(
            heading=(pl.arctan2(pl.col("delta_y"), pl.col("delta_x"))).degrees(),
            distance=(pl.col("delta_x") ** 2 + pl.col("delta_y") ** 2) ** 0.5,
        )
        .with_columns(
            velocity_kmh=(
                    pl.col("distance")
                    / pl.col("gps_sampling_rate").dt.total_seconds()
                    * 3.6
            )
        ).with_columns(
           is_outlier=pl.col("velocity_kmh") > min_outlier_kmh
        )
    )


def _filter_null_gps(df):
    return df.filter(pl.col("lat_raw").is_not_null() & pl.col("lon_raw").is_not_null())


def _linearize_geo(
        df: pl.DataFrame, linearization_coordinate: tuple[float, float] | None = None
) -> pl.DataFrame:
    """
    Flat Earth Linearization around the reference coordinate.
    Inaccurate for about 0.5% for distances ~20km. This might be an issue with downwind pumping.

    The motivation is to be able to work with intuitive units instead of the ~4th decimal of the coordinate.

    Besides, filters would have different behaviors depending on the latitude of the tracking.
    https://en.wikipedia.org/wiki/Latitude#Length_of_a_degree_of_latitude

    Thus, we should apply following logic/conditions on x/y and only use LAT/LON values for visualizations.
    """
    RADIUS_EARTH = 6_371_000
    if linearization_coordinate is None:
        linearization_coordinate = df.select(pl.min("lat_raw"), pl.min("lon_raw")).row(
            0
        )
    lat_ref, lon_ref = map(math.radians, linearization_coordinate)
    return df.with_columns(
        x=pl.lit(RADIUS_EARTH)
          * (pl.col("lon_raw").radians() - lon_ref)
          * math.cos(lat_ref),
        y=pl.lit(RADIUS_EARTH) * (pl.col("lat_raw").radians() - lat_ref),
    )
