import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import datetime as dt
from scipy.stats import zscore
import colorsys
import matplotlib.colors as mcolors

@st.cache_data
def load_data(filepath):
    """
    Load cleaned bank statement data.

    :param filepath: Path to the clean bank statement data (as .tsv).
    """
    data = pd.read_csv(filepath, sep="\t")
    data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce")
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Month"] = data["Date"].dt.strftime("%B")
    data = data.dropna(subset=["Year"])
    return data

# Function to generate color map
def generate_color_map(labels, palette):
    """
    Generate a color map for a given set of labels.

    :param labels: Unique labels to generate a color map for.
    :param palette: Color palette to use from plotly.
    """
    categories = labels.dropna().unique()
    return {category: palette[i % len(palette)] for i, category in enumerate(categories)}

# Function to apply common theming across plots.
def update_plot_layout(fig, type = None, fontsize = None, font_color = "black"):
    """
    Wrapper to update plotly plot themes automatically.

    :param fig: Plotly plot object.
    :param type: Type of plot: pie, heatmap.
    :param fontsize: Font size to apply generally.
    :param font_color: Font color to apply generally.
    """
    fig.update_layout(legend = dict(font = dict(size = fontsize),
                                    itemsizing = "constant"),
                      legend_title = dict(font = dict(size = fontsize)),
                      font = dict(size = fontsize, color = font_color),
                      plot_bgcolor = "white", 
                      paper_bgcolor = "white",
                      xaxis = dict(showline = True,
                                  ticks = "",
                                  tickfont = dict(size = fontsize, color = font_color),
                                  titlefont = dict(size = fontsize, color = font_color)),
                      yaxis = dict(showline = True,
                                  ticks = "",
                                  tickfont = dict(size = fontsize, color = font_color),
                                  titlefont = dict(size = fontsize, color = font_color)))
    
    if type == "pie":
        fig.update_layout(margin = dict(l = 0, r = 0, t = 20, b = 20),
                          showlegend = False,
                          height = 700)
    elif type == "heatmap":
        fig.update_layout(margin = dict(l = 0, r = 0, t = 50, b = 0),
                          coloraxis_colorbar = dict(title = dict(font = dict(size = fontsize, color = font_color)),
                                                    tickfont = dict(size = fontsize, color = font_color)))
    elif type == "treemap":
        fig.update_layout(uniformtext = dict(minsize = fontsize, mode = "hide"),
                          margin = dict(t = 50, l = 25, r = 25, b = 25),
                          height = 800,
                          coloraxis_colorbar = dict(title = dict(font = dict(size = fontsize, color = font_color)),
                                                    tickfont = dict(size = fontsize, color = font_color)))

        
    return fig

def hex_to_rgb(hex_color):
    """
    Convert a hex color to an RGB tuple.
    :param hex_color: Hex color string (e.g., "#FF0000").
    :return: Tuple of RGB values in the range [0, 1].
    """
    return mcolors.hex2color(hex_color)

def desaturate_color(color, factor = 0.5):
    """
    Desaturates a single color by the given factor.
    :param color: Tuple of RGB values (r, g, b), each in the range [0, 1].
    :param factor: Desaturation factor (0 = completely desaturated, 1 = original saturation).
    :return: Tuple of desaturated RGB values.
    """
    r, g, b = color
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s *= factor

    return colorsys.hls_to_rgb(h, l, s)

def desaturate_colors(colors, factor = 0.5):
    """
    Desaturates a list of colors.
    :param colors: List of hex color strings or RGB tuples.
    :param factor: Desaturation factor (0 = completely desaturated, 1 = original saturation).
    :return: List of desaturated RGB values.
    """
    rgb_colors = [hex_to_rgb(color) if isinstance(color, str) else color for color in colors]
    return [desaturate_color(color, factor) for color in rgb_colors]

def create_colorscale_from_colors(colors):
    """
    Converts a list of RGB tuples to a Plotly-compatible colorscale.
    :param colors: List of RGB tuples.
    :return: List of [value, color] pairs for colorscale.
    """
    n = len(colors)
    return [[i / (n - 1), mcolors.rgb2hex(color)] for i, color in enumerate(colors)]