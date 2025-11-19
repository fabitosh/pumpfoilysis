import polars as pl


def calc_session_summary(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculates summary statistics for each pump run.
    Expects a DataFrame with 'is_pumping', 'datetime', 'distance', and 'velocity_kmh' columns.
    """
    # Change in is_pumping indicates a new pump session
    df = df.with_columns(
        run_id=(
            pl.col("is_pumping")
            .ne(pl.col("is_pumping").shift(1))
            .fill_null(False)
            .cast(pl.UInt32)
            .cum_sum()
        )
    )

    df_runs = df.filter(pl.col("is_pumping"))

    if df_runs.is_empty():
        return pl.DataFrame(
            schema={
                "run_id": pl.UInt32,
                "start_time": pl.Datetime,
                "duration_s": pl.Float64,
                "distance_m": pl.Float64,
                "max_speed_kmh": pl.Float64,
                "avg_speed_kmh": pl.Float64,
            }
        )

    summary = (
        df_runs.group_by("run_id")
        .agg(
            start_time=pl.col("datetime").min(),
            duration_s=(
                pl.col("datetime").max() - pl.col("datetime").min()
            ).dt.total_seconds(),
            distance_m=pl.col("distance").sum(),
            max_speed_kmh=pl.col("velocity_kmh").max(),
            avg_speed_kmh=pl.col("velocity_kmh").mean(),
        )
        .sort("start_time")
    )

    return summary
