from .utils import *
import plotly.express as px
import seaborn as sns

# Function to generate scatter plot.
def treemap_plot(data, options, continuous_palette):
    """
    Generate a treemap plot based on given data.

    :param data: Data to plot.
    :param options: Dictionary with the user-provided streamlit options.
    :continuous_palette: Discrete color palette to use. 
    """

    data_plot = data.groupby(["Sector", "Category", "Group"])["Amount"].sum().reset_index()

    p = px.treemap(data_plot, 
                   path=[px.Constant("Expenses"), "Sector", "Category", "Group"],
                   values = "Amount",
                   color = "Amount", 
                   hover_data = ["Amount"],
                   range_color = [0, data_plot["Amount"].quantile(0.975)],
                   color_continuous_scale = continuous_palette)
    
    p.update_traces(marker = dict(cornerradius = 5, line = dict(width = 1.5)))

    p = update_plot_layout(fig = p, font_size = options["Fontsize"], type = "treemap")

    return p