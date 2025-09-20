import polars as pl

# Schema for the initial raw data parsed from .fit or .tcx files
# Raw values should remain untouched after the parsing step.
SCHEMA_RAW = {
    "datetime": pl.Datetime(time_unit="ms"),
    "lat_raw": pl.Float64,
    "lon_raw": pl.Float64,
    "altitude_raw": pl.Float64,
}

SCHEMA_REFINED = {
    **SCHEMA_RAW,
    # refined values after a gps refinement
    "lat": pl.Float64,
    "lon": pl.Float64,
    "velocity_kmh": pl.Float64,
    "is_outlier": pl.Boolean,  # set refined coordinates to NULL
}

# Final schema after categorization
SCHEMA_CLASSIFIED = {
    **SCHEMA_REFINED,
    "state": pl.Enum(["On Foil", "Other"]),
    "event": pl.Enum(["Start", "Pump", "Surf", "Fail"]),
}
