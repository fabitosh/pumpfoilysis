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
