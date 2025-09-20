import math

import polars as pl



def linearize_geo(
    df: pl.DataFrame, linearization_coordinate: tuple[float, float] | None = None
) -> pl.DataFrame:
    """
    Flat Earth Linearization around the reference coordinate.
    Inaccurate for about 0.5% for distances ~20km. This might be an issue with downwind pumping.


def calc_refine_features(df: pl.DataFrame) -> pl.DataFrame:
    cols_gps = ["lat_raw", "lon_raw"]
    df_idx = _calc_generic_features(df.drop(cols_gps))
    df_gps = _filter_null_gps(df).select(["datetime"] + cols_gps)
    return df_idx.join(_calc_gps_features(df_gps), on="datetime", how="left")


def _calc_generic_features(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        sampling_rate=pl.col("datetime").diff(),
        # delta_distance_raw=pl.col("distance_raw").diff(),  # todo: remove later
    )


def _calc_gps_features(df: pl.DataFrame) -> pl.DataFrame:
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
            .fill_null(0)
            .alias("speed_kmh")
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


def reject_gps_outliers(
        df: pl.DataFrame, max_speed_kmh: float = SPEED_OUTLIER_KMH
) -> pl.DataFrame:
    df
