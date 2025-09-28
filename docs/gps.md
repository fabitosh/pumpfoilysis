# GPS 

This documents notes down discovered challenges in the tracked GPS data and how they are addressed.
So far, this is only from looking into the data from the Garmin Forerunner 945 LTE.

## Data Gaps
In one session at an open spot, 3755 missing GPS points for 6636 are found.
LAT and LON values are identically missing. 

Plotting the occurrences of the missing values, it appears to correlate with times where I fell into water. Yet, not exclusively.

```python
has_nan = df.get_column("lat_raw").is_null()
dfill = df.with_columns(pl.col(['lat_raw', 'lon_raw']).fill_null(strategy='forward').fill_null(strategy='backward'))
fig_debug = px.line_map(dfill.with_columns(is_nan=has_nan), lat='lat_raw', lon='lon_raw', color='is_nan', zoom=17, height=800)
fig_debug.update_layout(map_style="open-street-map")
```

### Handling the gaps
Options for handling the GPS gaps would be:

- Keep them null and let algos decide how to handle them. -> chosen for now. There is not enough understanding of
  the patterns yet.
- Backward/forward-fill the gaps.
- Interpolate the data gaps between the last and first known locations around GPS gaps. I would assume that the
  first known locations would be more likely to be inaccurate or outliers.
- Drop rows with GPS gaps early in the pipeline. This would also drop data such as HR and other sensor data that
  could be useful.

We need to make sure that refined metrics such as the velocity calculation is aware of inconsistent sampling frequency.

## Outliers
Most impactful outliers are characterized by short and big jumps in position.
An easy first filter is the rejection by comparison with maximum expected speeds.

## Drift

Some runs seem to be consistently off by a few meters.
One can identify them when a session starts ~10m away from the starting dock,
but consistently so over multiple following datapoints.
Basically the run in itself has no visible issue.

## TCX provided distance and speed values

The `.tcx` files of my watch come with `distance` and `speed` values for most rows.
They have already gone through some form of processing and don't match the deltas of the raw GPS data.
We will use them as comparison to find corner cases, but will not have any reliance on it.

- The analysis should work on raw GPS data only.
- I'd rather create, understand and be able to tweak the processing.