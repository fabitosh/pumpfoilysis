import polars as pl


def calc_rolling_metrics(df: pl.DataFrame, window_size: str) -> pl.DataFrame:
    df = df.with_columns(
        velocity_smoothed=pl.mean("velocity_kmh").rolling(
            index_column="datetime", period=window_size
        ),
        # todo: circular std for heading needed
        heading_std=pl.std("heading").rolling(
            index_column="datetime", period=window_size
        ),
    ).with_columns(
        velocity_smoothed=pl.when(pl.col("lat_raw").is_null())
        .then(pl.lit(None).cast(pl.Float64))
        .otherwise(pl.col("velocity_smoothed")),
        heading_std=pl.when(pl.col("lat_raw").is_null())
        .then(pl.lit(None).cast(pl.Float64))
        .otherwise(pl.col("heading_std")),
    )
    return df


# def categorize(df: pl.DataFrame, )
