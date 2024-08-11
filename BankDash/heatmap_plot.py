from.utils import *

# Function to generate the heatmap.
def heatmap_plot(data, scale_data, focus, continuous_palette, divergent_palette, fontsize):
    """
    Generate a heatmap plot based on given data.

    :param data: Data to plot.
    :param focus: Category to focus.
    :continuous_palette: Continuous color palette to use. 
    :divergent_palette: Divergent color palette to use.
    :scale_data: Whether to Z-score the heatmap data.
    :param fontsize: Font size to use in the plot.
    """

    data_plot_heatmap = data.groupby([focus, "Month"])["Amount"].sum().reset_index()

    # Reorder months
    month_order = ["January", "February", "March", "April", "May", "June", "July", 
                   "August", "September", "October", "November", "December"]
    
    unique_months = list(set(data_plot_heatmap["Month"].tolist()))
    month_values_use = [month for month in month_order if month in unique_months]

    data_plot_heatmap["Month"] = pd.Categorical(data_plot_heatmap["Month"], categories = month_values_use, ordered = True)
                      
    data_wide = data_plot_heatmap.pivot(index = "Month", columns = focus, values = "Amount")
    data_wide.fillna(0, inplace = True)
        
    p = px.imshow(data_wide if scale_data == "No" else data_wide.apply(zscore),
                  labels = dict(x = focus,
                                y = "Category",
                                color = "Amount"),
                  x = data_wide.columns,
                  y = data_wide.index,
                  zmax = 350 if scale_data == "No" and focus != "Sector" else None,
                  color_continuous_midpoint = None if scale_data == "No" else 0,
                  color_continuous_scale = continuous_palette if scale_data == "No" else divergent_palette)
        
    p.update_traces(xgap = 1.5, 
                    ygap = 1.5, 
                    selector = dict(type = "heatmap"))
    
    p = update_plot_layout(fig = p, type = "heatmap", fontsize = fontsize)

    return p