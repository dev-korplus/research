# CSS Color Scheme Integration for Plotly
import polars as pl
import numpy as np
from plotly import graph_objects as go
import plotly.express as px
from typing import List
import kaleido
import plotly.figure_factory as ff
import plotly.io as pio
import os
from pathlib import Path


def get_plotly_theme():
    """Create Plotly theme configuration from CSS color scheme"""
    colors = {
        "background": "#ffffff",  # oklch(1 0 0)
        "foreground": "#252525",  # oklch(0.145 0 0)
        "card": "#ffffff",  # oklch(1 0 0)
        "primary": "#343434",  # oklch(0.205 0 0)
        "secondary": "#f7f7f7",  # oklch(0.97 0 0)
        "muted": "#f7f7f7",  # oklch(0.97 0 0)
        "accent": "#f7f7f7",  # oklch(0.97 0 0)
        "border": "#d0d0d0",  # oklch(0.82 0 0)
        "destructive": "#e2483d",  # oklch(0.577 0.245 27.325)
    }

    return {
        "layout": {
            "paper_bgcolor": colors["background"],
            "plot_bgcolor": colors["card"],
            "font": {
                "family": "Source Code Pro, monospace",
                "color": colors["foreground"],
                "size": 10,
            },
            "title": {
                "font": {
                    "family": "Source Code Pro, monospace",
                    "color": colors["foreground"],
                    "size": 24,
                }
            },
            "xaxis": {
                "gridcolor": colors["border"],
                "gridwidth": 0.5,
                "linecolor": colors["border"],
                "linewidth": 0.5,
                "tickcolor": colors["border"],
                "title_font": {"color": colors["foreground"]},
                "tickfont": {"color": colors["foreground"]},
                "zeroline": True,
                "zerolinecolor": colors["border"],
                "zerolinewidth": 0.5,
            },
            "yaxis": {
                "gridcolor": colors["border"],
                "gridwidth": 0.5,
                "linecolor": colors["border"],
                "linewidth": 0.5,
                "tickcolor": colors["border"],
                "title_font": {"color": colors["foreground"]},
                "tickfont": {"color": colors["foreground"]},
                "zeroline": True,
                "zerolinecolor": colors["border"],
                "zerolinewidth": 0.5,
            },
            "legend": {
                "bgcolor": colors["card"],
                "bordercolor": colors["border"],
                "font": {"color": colors["foreground"]},
            },
        }
    }


# Create theme configuration
PLOTLY_THEME = get_plotly_theme()

# Chart color palette based on your CSS chart colors + secondary palette
CHART_COLORS = [
    # Primary CSS colors
    "#d97706",
    "#0891b2",
    "#7c3aed",
    "#65a30d",
    "#ca8a04",
    # Secondary palette - darker and richer
    "#E53E3E",
    "#38B2AC",
    "#3182CE",
    "#68D391",
    "#F6AD55",
    "#B794F6",
    "#4FD1C7",
    "#F6E05E",
    "#9F7AEA",
    "#63B3ED",
    "#F687B3",
    "#48BB78",
]


# CSS-Integrated Plotly Functions


def update_layout(fig: go.Figure, title: str):
    """
    Update Plotly figure layout with CSS-integrated theme

    Args:
        fig: Plotly figure object
        title: Chart title
    """
    fig.update_layout(**PLOTLY_THEME["layout"])
    fig.update_layout(title=title)

    # Update trace colors to use theme colors
    for i, trace in enumerate(fig.data):
        if hasattr(trace, "line") and trace.line:
            trace.line.color = CHART_COLORS[i % len(CHART_COLORS)]
        elif hasattr(trace, "marker") and trace.marker:
            trace.marker.color = CHART_COLORS[i % len(CHART_COLORS)]

    # Configure legend
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )

    return fig


def export_png_high_quality(
    fig: go.Figure,
    filename: str,
    width: int = 1200,
    height: int = 800,
    scale: float = 2.0,
):
    """
    Export Plotly figure as high-quality PNG while preserving all custom styling

    Args:
        fig: Plotly figure object
        filename: Output filename (with or without .png extension, can include directory path)
        width: Image width in pixels (default: 1200)
        height: Image height in pixels (default: 800)
        scale: Scale factor for higher DPI (default: 2.0 = 2x resolution)

    Returns:
        str: Path to exported file
    """
    # Ensure filename has .png extension
    if not filename.endswith(".png"):
        filename += ".png"
    
    # Create directory if it doesn't exist
    file_path = Path(filename)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Export with high quality settings
    fig.write_image(
        str(file_path),
        width=width,
        height=height,
        scale=scale,
        format="png",
        engine="kaleido",
    )

    return str(file_path)


def export_png(fig: go.Figure, filename: str, width: int = 1200, height: int = 800, scale: float = 1.0):
    """
    Export Plotly figure as PNG with custom dimensions and scale
    
    Args:
        fig: Plotly figure object
        filename: Output filename (with or without .png extension)
        width: Image width in pixels (default: 1200)
        height: Image height in pixels (default: 800)
        scale: Scale factor for higher DPI (default: 1.0)
    
    Returns:
        str: Path to exported file
    """
    return export_png_high_quality(fig, filename, width, height, scale)


def plot_lines(
    df: pl.DataFrame,
    title: str,
    theme: str = "light",
    x_col: str = "ts",
    y_cols: List[str] = ["p"],
    x_axis_title: str = "Date",
    y_axis_title: str = "Commits (Monthly)",
):
    fig = go.Figure()

    for y_col in y_cols:
        fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode="lines", name=y_col))

    update_layout(fig, title)
    fig.update_layout(title=title, xaxis_title=x_axis_title, yaxis_title=y_axis_title)
    return fig


if __name__ == "__main__":
    df = pl.DataFrame(
        {
            "ts": np.arange(100),
            "y1": np.sin(np.log(np.arange(100) + 1)) * 2,
            "y2": np.exp(np.sin(np.arange(100) / 10)) - 2,
            "y3": np.log(np.arange(100) + 1) * np.sin(np.arange(100) / 5),
        }
    )

    fig = plot_lines(
        df=df,
        title="Commits by Month",
        theme="light",
        x_col="ts",
        y_cols=["y1", "y2", "y3"],
        x_axis_title="Date",
        y_axis_title="Commits (Monthly)",
    )

    # Export examples
    print("📸 Testing PNG export functions:")
    export_png_web_quality(fig, "commits_web_quality")
    export_png_high_quality(fig, "commits_custom", width=1600, height=1000, scale=2.5)

    fig.show()
