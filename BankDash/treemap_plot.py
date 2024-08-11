from .utils import *
import plotly.express as px
import seaborn as sns

# Function to generate scatter plot.
def treemap_plot(data, continuous_palette, fontsize):
    """
    Generate a treemap plot based on given data.

    :param data: Data to plot.
    :continuous_palette: Discrete color palette to use.  
    :param fontsize: Font size to use in the plot.
    """

    data_plot = data.groupby(["Sector", "Category", "Group"])["Amount"].sum().reset_index()
    
    p = px.treemap(data_plot, 
                   path=[px.Constant("Expenses"), "Sector", "Category", "Group"],
                   values = "Amount",
                   color = "Amount",
                   range_color = [0, data_plot["Amount"].quantile(0.975)],
                   color_continuous_scale = continuous_palette,
                   hover_name = None,
                   hover_data={'Sector': False, 'Category': False, 'Group': False, "Amount": False})  # Customize hover labels)
    # Update layout to suppress unwanted default labels
    parent = p.data[0].parents.tolist()
    parent = [i.split('/')[-1] for i in parent]

    customdata = pd.DataFrame()
    customdata["Name"] = p.data[0].labels
    customdata["Parents"] = parent
    customdata["Values"] = p.data[0].values
    p.update_traces(marker = dict(cornerradius = 5, line = dict(width = 1.5, color = "black")),
                    hovertemplate="<b>%{customdata[0]}</b><br><br>" + 
                                  "<b>Parent:</b> %{customdata[1]}<br>" + 
                                  "<b>Amount:</b> %{customdata[2]:,.2f} €<br>" + 
                                  "<extra></extra>",  # Customize hover template
                    customdata = customdata)

    p = update_plot_layout(fig = p, fontsize = fontsize, type = "treemap")

    return p