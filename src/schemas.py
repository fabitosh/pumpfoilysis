import polars as pl

# Schema for the initial raw data parsed from .fit or .tcx files
SCHEMA_RAW = {
    "timestamp": pl.Datetime(time_unit="ms"),
    "lat_raw": pl.Float64,
    "lon_raw": pl.Float64,
    "altitude_raw": pl.Float64,
}

# Schema after refining and adding calculated columns
SCHEMA_REFINED = {
    **SCHEMA_RAW,
    "lat": pl.Float64,
    "lon": pl.Float64,
    "velocity_kmh": pl.Float64,
    "distance_m": pl.Float64,
    "is_outlier": pl.Boolean,  # set refined coordinates to NULL
}

# Final schema after categorization
SCHEMA_CLASSIFIED = {
    **SCHEMA_REFINED,
    "state": pl.Enum(["On Foil", "Other"]),
    "event": pl.Enum(["Start", "Pump", "Surf", "Fail"]),
}
