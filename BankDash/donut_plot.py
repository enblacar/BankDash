from .utils import *

# Function to generate the donut chart.
def donut_plot(data, options, discrete_palette):
    """
    Generate a donut plot based on given data.

    :param data: Data to plot.
    :param options: Dictionary with the user-provided streamlit options.
    :discrete_palette: Discrete color palette to use. 
    """

    # Filter data based on month
    data_plot = data if options["Month"] == "All months" else data[data["Month"] == options["Month"]]

    if options["Subset"] == "None":
        group_by_column = options["Focus"]
    else:
        group_by_column = {"Sector": "Category", "Category": "Group", "Group": "Payee"}[options["Focus"]]
        data_plot = data_plot[data_plot[options["Focus"]] == options["Subset"]]
    
    data_plot = data_plot.groupby(group_by_column)["Amount"].sum().reset_index().sort_values("Amount", ascending = True)

    # Group small categories into "Other"
    total_value = data_plot["Amount"].sum()
    threshold = 0.035 * total_value
    data_plot[group_by_column] = data_plot.apply(lambda x: x[group_by_column] if x["Amount"] >= threshold else "Other", axis=1)
    data_plot = data_plot.groupby(group_by_column).sum().sort_values(by = "Amount", ascending = True).reset_index()

    color_map = generate_color_map(data_plot[group_by_column], discrete_palette)
    colors = [color_map[label] for label in data_plot[group_by_column]]

    p = go.Pie(labels = data_plot[group_by_column],
               values = data_plot["Amount"],
               hole = 0.75,
               textinfo = "label",
               hoverinfo = "percent + value",
               title = f'Expenses by <b>{options["Focus"]}</b><br><b>{options["Year"]}</b> | <b>{options["Month"]}</b> | <b>{options["Subset"]}</b>',
               marker = dict(colors = colors,
                             line = dict(color = "white", 
                                         width = 1.5)))  
    
    p = go.Figure(p)

    p = update_plot_layout(fig = p, type = "pie", font_size = options["Fontsize"])

    return p