from BankDash import *
import streamlit as st
import plotly.express as px

def main():
    # Set streamlit page config.
    st.set_page_config(layout = "wide",
                       page_icon = "random",
                       page_title = "Bank Eagle View")
    

    # Define pages.
    p1 = st.Page(page = "./pages/1_page_donut_plot.py", title = "Donut plot", icon = ":material/query_stats:")
    p2 = st.Page(page = "./pages/2_page_heatmap_plot.py", title = "Heatmap", icon = ":material/query_stats:")
    p3 = st.Page(page = "./pages/3_page_scatter_plot.py", title = "Scatter plot", icon = ":material/query_stats:")
    p4 = st.Page(page = "./pages/4_page_treemap_plot.py", title = "Treemap plot", icon = ":material/query_stats:")
    p5 = st.Page(page = "./pages/5_page_calculate_future_value.py", title = "Compound interest calculator", icon = ":material/query_stats:")

    

    # Load and preprocess data (use caching to speed up reloads)
    data = load_data("/Users/e420a/Desktop/BankDash/data/bank_statements_clean.tsv")
    if "data" not in st.session_state:
        st.session_state.data = data
    
    # Define color palettes.
    discrete_palette = ["whitesmoke"] + px.colors.sequential.ice_r + ["black"]
    if "discrete_palette" not in st.session_state:
        st.session_state.discrete_palette = discrete_palette

    discrete_palette_2 = px.colors.qualitative.Prism + px.colors.qualitative.Vivid
    if "discrete_palette_2" not in st.session_state:
        st.session_state.discrete_palette_2 = discrete_palette_2
        
    continuous_palette = ["whitesmoke"] + px.colors.sequential.YlGnBu + ["black"]
    if "continuous_palette" not in st.session_state:
        st.session_state.continuous_palette = continuous_palette

    divergent_palette = px.colors.sequential.RdBu_r
    if "divergent_palette" not in st.session_state:
        st.session_state.divergent_palette = divergent_palette

    # Initialize the slider value in session state if not already set
    if 'fontsize' not in st.session_state:
        st.session_state.fontsize = 16  # Default value
    # Display the slider in the sidebar and update session state
    st.session_state.fontsize = st.sidebar.slider("Plot font size:", min_value = 8, max_value = 24, value = 16, step = 1)
    
    
    # Install multipage:
    pg = st.navigation(dict(Finances = [p1, p2, p3, p4],
                            Calculators = [p5]))
    pg.run()    

if __name__ == "__main__":
    main()