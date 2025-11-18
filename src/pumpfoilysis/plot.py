import polars as pl
import plotly.express as px
import plotly.graph_objs as go


def get_run_fig(df: pl.DataFrame, color_col: str = "is_outlier") -> go.Figure:
    fig = px.line_map(
        df, lat="lat_raw", lon="lon_raw", color=color_col, zoom=17, height=800, hover_data=["datetime", "velocity_kmh"]
    )
    fig.update_layout(map_style="open-street-map")
    return fig
