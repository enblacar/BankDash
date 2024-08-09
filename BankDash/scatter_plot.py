from .utils import *

# Function to generate scatter plot.
def scatter_plot(data, options, discrete_palette):
    """
    Generate a scatter plot based on given data.

    :param data: Data to plot.
    :param options: Dictionary with the user-provided streamlit options.
    :discrete_palette: Discrete color palette to use. 
    """

    color_map = generate_color_map(data[options["Focus"]], discrete_palette)

    p = px.scatter(data,
                   x = "Date",
                   y = "Amount",
                   color = options["Focus"],
                   color_discrete_map = color_map,
                   log_y = True)
    p.update_traces(marker = dict(size = 12, line = dict(color = "black", width = 1.5)))


    p = update_plot_layout(fig = p, font_size = options["Fontsize"])

    p.update_layout(height = 800)
    return p