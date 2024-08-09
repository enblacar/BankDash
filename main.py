from BankDash import *
import streamlit as st
import plotly.express as px

def main():
    # Set streamlit page config.
    st.set_page_config(layout = "wide",
                    page_icon = "random",
                    page_title = "Bank Eagle View")

    # Load and preprocess data (use caching to speed up reloads)
    data = load_data("/Users/e420a/Desktop/BankDash/data/bank_statements_clean.tsv")

    # Define color palettes.
    discrete_palette = ["whitesmoke"] + px.colors.sequential.ice_r + ["black"]
    discrete_palette_2 = px.colors.qualitative.Prism + px.colors.qualitative.Vivid
    continuous_palette = ["whitesmoke"] + px.colors.sequential.YlGnBu + ["black"]
    divergent_palette = px.colors.sequential.RdBu_r

    # Sidebar options
    year_options = data['Year'].unique().astype(int)
    option_year = st.sidebar.radio('Filter by Year:', year_options, key = "year1", index = len(year_options) - 1)
    option_focus = st.sidebar.radio("Choose a focus:", ["Sector", "Category", "Group"], key = "focus1", index = 1)
    option_fontsize = st.sidebar.slider("Plot font size:", min_value = 8, max_value = 24, value = 16, step = 1)

    options = {"Year": option_year,
            "Focus": option_focus,
            "Fontsize": option_fontsize}

    # Filter data based on selected year
    filtered_data = data[data["Year"] == options["Year"]]

    # Generate master tabs.
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pie", "Heat", "Cloud", "Tree", "Future Value"])


    with tab1:
        
        col1, col2 = st.columns([2, 8])
        with col1:
            # Pie options.
            option_subset = st.selectbox("Choose a Subset:", ["None"] + sorted(data[options["Focus"]].dropna().unique().tolist()), key="subset1")
            option_month = st.selectbox("Choose a Month:", ["All months"] + data[data["Year"] == options["Year"]]["Month"].dropna().unique().tolist())

            options["Subset"] = option_subset
            options["Month"] =  option_month
            
        with col2:        
            p = donut_plot(data = filtered_data, options = options, discrete_palette = discrete_palette)

            st.plotly_chart(p, use_container_width = True)

    with tab2:
        # Scale data?
        scale_data = st.radio("Z-Score?", ["No", "Yes"], key = "scale1", horizontal = True)

        p = heatmap_plot(data = filtered_data, scale_data = scale_data, options = options, continuous_palette = continuous_palette, divergent_palette = divergent_palette)
        
        st.plotly_chart(p, use_container_width = False)
            
    with tab3:
        p = scatter_plot(data = filtered_data, options = options, discrete_palette = discrete_palette_2)

        st.plotly_chart(p, use_container_width = True)

    with tab4:
        p = treemap_plot(data = data, options = options, continuous_palette = ["gainsboro"] + px.colors.sequential.YlGnBu)
        
        st.plotly_chart(p, use_container_width = True)

    with tab5:

        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1: 
                principal = st.number_input("Initial investment (€)", min_value = 0, value = None, step = 50, placeholder = "1500", help = "Amount in Euros")
                contribution = st.number_input("Contribution (€)", min_value = 0, value = None, step = 50, placeholder = "100", help = "Recurrent contribution")
            with col2: 
                times_compounded = st.number_input("Times compounded", min_value = 1, value = None, placeholder = "12", help = "How many times the interest compounds")
                years = st.number_input("Years", min_value = 1, value = None, placeholder = "35", help = "Time horizon")
            with col3:
                annual_rate = st.number_input("Annual Growth Rate (%)", min_value = 0.00, value = None, step = 0.01, placeholder = "5.0", help = "Expected annual growth rate")
                ter = st.number_input("TER (%)", min_value = 0.00, value = 0.00, step = 0.01, placeholder = "0.22", help = "Total Expense Ratio, from a given ETF. Use 0 otherwise.")
            with col4:
                " "
                " "
                " "
                inflation = st.toggle("Account for inflation?", help = "This substracts an average 2% inflation to the annual rate provided.")
                
                log_y = st.toggle("Log scale?", help = "Log 10 scale the Y axis.")
                
            variables_check = [principal, contribution, times_compounded, years, annual_rate, ter]
           
        if all(x is not None for x in variables_check):
            amount = calculate_future_value(principal = principal, 
                                        annual_rate = annual_rate, 
                                        times_compounded = times_compounded, 
                                        years = years, 
                                        contribution = contribution,
                                        ter = ter, 
                                        inflation = inflation)
            
            p = plot_future_values(data = amount, options = options, discrete_palette = discrete_palette_2, log_y = log_y)
            
            st.plotly_chart(p, use_container_width=True)
        else:
            st.info('Please fill the **empty input fields**. Once done, the plot will **update automatically** every time you **modify** a value.', icon="🔜")

            

if __name__ == "__main__":
    main()