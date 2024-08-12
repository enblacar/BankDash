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
import plotly.colors as pc

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

def get_plotly_colors():
    # Create a dictionary of the colors for each color palette in plotly.
    qualitative_colors = {palette_name: getattr(px.colors.qualitative, palette_name)
                         for palette_name in dir(px.colors.qualitative)
                         if not palette_name.startswith("_") and isinstance(getattr(px.colors.qualitative, palette_name), list)}

    sequential_colors = {palette_name: getattr(px.colors.sequential, palette_name)
                        for palette_name in dir(px.colors.sequential)
                        if not palette_name.startswith("_") and isinstance(getattr(px.colors.sequential, palette_name), list)}
    
    diverging_colors = {palette_name: getattr(px.colors.diverging, palette_name)
                        for palette_name in dir(px.colors.diverging)
                        if not palette_name.startswith("_") and isinstance(getattr(px.colors.diverging, palette_name), list)}
    
    return qualitative_colors, sequential_colors, diverging_colors

def display_palette_as_gradient(palette, continuous = True, num_colors = 100):
    # Create a continuous color scale based on the selected qualitative palette
    color_scale = pc.make_colorscale(palette)
    if continuous:
        colors_use = pc.sample_colorscale(color_scale, [i/(num_colors-1) for i in range(num_colors)], colortype='rgb')
    else:
        colors_use = palette

    # Prepare an HTML string to render the color scale as a single line of div elements
    color_boxes = ''.join(
        f'<div style="background-color:{color}; height:50px; width:100%; flex:1; margin:0; padding:0;"></div>'
        for color in colors_use
    )

    # Display the color scale as a single horizontal line
    st.write(f'<div style="display:flex; width:100%;">{color_boxes}</div>', unsafe_allow_html=True)
    