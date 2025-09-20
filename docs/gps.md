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
- Keep them nan and let algos decide how to handle them. -> chosen for now
- Backward/forward-fill the gaps.
- Interpolate the data gaps between the known locations. Are the known locations around more likely to be outliers?
- Drop rows with gaps. This would also drop data such as HR and other sensor data that could be useful features.

We need to make sure that refined metrics such as the velocity calculation is aware that the sampling frequency has 
not been consistent.

## Outliers
Most impactful outliers are characterized by short and big jumps in position.
An easy first filter is the rejection by comparison with maximum expected speeds.


## TCX provided distance and speed values
Already went through some form of processing and don't match the raw GPS data. We will use them as comparison to find corner cases, but will not have any reliance on it.
- The analysis should work with the raw GPS data only.
- I'd rather create, understand and be able to tweak the processing.