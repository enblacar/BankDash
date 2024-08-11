from .utils import *

# Function to generate scatter plot.
def scatter_plot(data, focus, discrete_palette, fontsize):
    """
    Generate a scatter plot based on given data.

    :param data: Data to plot.
    :param focus: Focus to use.
    :param discrete_palette: Discrete color palette to use. 
    :param fontsize: Font size to use in the plot.
    """

    color_map = generate_color_map(data[focus], discrete_palette)

    p = px.scatter(data,
                   x = "Date",
                   y = "Amount",
                   color = focus,
                   color_discrete_map = color_map,
                   log_y = True)
    p.update_traces(marker = dict(size = 12, line = dict(color = "black", width = 1.5)))


    p = update_plot_layout(fig = p, fontsize = fontsize)

    p.update_layout(height = 800)
    return p