from .utils import *

def plot_future_values(data, options, discrete_palette, log_y):
    """
    Plot the future values as a stacked bar plot using Plotly.

    :param data: DataFrame containing the future value data.
    :param options: Dictionary with the user-provided streamlit options.
    :param discrete_palette: Discrete color palette to use. 
    :param log_y: Whether to log10 scale the Y axis.
    """

    # Turn wide data to long data.
    data_long = pd.melt(data.loc[:, ["Year", "Initial Investment", "Contributions", "Interest", "Total"]],
                        id_vars = "Year",
                        var_name = "Type",
                        value_name = "Amount")
    
    # Calculate the total amount per Year
    totals = data_long.groupby("Year")["Amount"].sum().reset_index()
    totals.rename(columns = {"Amount": "Total"}, inplace = True)
    

    # Merge the total amounts back into the original DataFrame
    data_long = data_long.merge(totals, on = "Year")
    color_map = generate_color_map(data_long["Type"], discrete_palette)
    color_map["Total"] = "white"

    p = px.bar(data_frame = data_long,
               x = "Year",
               y = "Amount",
               color = "Type",
               text_auto = False,
               title = None,
               color_discrete_map = color_map,
               custom_data = ["Type", "Total"],
               log_y = log_y) 
    

    p.update_traces(marker = dict(line = dict(color = "white", width = 1)),
                    hovertemplate = '<b>%{customdata[0]}:</b> %{y:,.2f} €' +
                                     '<extra></extra>')
    

    # Surgically insert things in the hover :D.
    p.data[3].update(customdata = data_long.loc[:, ["Year", "Total"]],
                     hovertemplate = '<b>Total:</b> %{customdata[1]:,.2f} €'+
                                     '<extra></extra>',
                     showlegend =  False,
                     marker = dict(line = dict(color = "white", width = 1)))

    # Update layout
    p.update_layout(xaxis_title = 'Year',
                    yaxis_title = 'Total (€)',
                    legend_title = "",
                    bargap = 0.2,
                    hovermode = "x unified",
                    hoverlabel=dict(bgcolor="white", font_size=options["Fontsize"]),
                    legend = dict(x = 0.5, y = 1.1, xanchor = "center", yanchor = "top", orientation = "h"),
                          height = 700)

    p = update_plot_layout(fig = p, type = "bar", font_size = options["Fontsize"])
    

    return(p)