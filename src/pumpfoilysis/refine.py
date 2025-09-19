import math

import polars as pl


def linearize_geo(
    df: pl.DataFrame, linearization_coordinate: tuple[float, float] | None = None
) -> pl.DataFrame:
    """Flat Earth Linearization around the reference coordinate. Inaccurate for distances > ~20km"""
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
