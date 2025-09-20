import math

import polars as pl



def linearize_geo(
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
