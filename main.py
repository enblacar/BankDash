import streamlit as st
import plotly.express as px
from BankDash import *

def main():
    # Set Streamlit page configuration
    st.set_page_config(layout="wide", page_icon="random", page_title="Bank Eagle View")

    # Define pages
    p1 = st.Page(page="./pages/1_page_donut_plot.py", title="Donut plot", icon=":material/query_stats:")
    p2 = st.Page(page="./pages/2_page_heatmap_plot.py", title="Heatmap", icon=":material/query_stats:")
    p3 = st.Page(page="./pages/3_page_scatter_plot.py", title="Scatter plot", icon=":material/query_stats:")
    p4 = st.Page(page="./pages/4_page_treemap_plot.py", title="Treemap plot", icon=":material/query_stats:")
    p5 = st.Page(page="./pages/5_page_calculate_future_value.py", title="Compound interest calculator", icon=":material/query_stats:")

    # Load and preprocess data (use caching to speed up reloads)
    @st.cache_data
    def get_data():
        return load_data("/Users/e420a/Desktop/BankDash/data/bank_statements_clean.tsv")

    data = get_data()
    if "data" not in st.session_state:
        st.session_state.data = data

    # Generate a header toolkit
    with st.expander("**Theme options**"):

        with st.container():
            col1, col2 = st.columns([2, 8], gap="small", vertical_alignment = "center")  # Specify the gap explicitly to avoid default behavior

            # Display the slider in the sidebar and update session state
            with col1:
                fontsize_value = st.slider("**Font size**", min_value=8, max_value=24, value=16, step=1, key="fontsize_slider", help = "Controls the overall font size across all elements in the plots.")
                add_palette_ends = st.toggle("B/W ends", help = "Adds white and black ends to continuous color palettes so that the range of colors is concentrated on the middle values of the scale.")
            with col2:
                # Display color palettes
                plotly_qualitative, plotly_sequential, plotly_divergent = get_plotly_colors()

                with st.container():
                    col1, col2 = st.columns([2, 8], gap="small", vertical_alignment = "center")

                    # Use a key for each selectbox to ensure unique storage in session state
                    with col1:
                        discrete_colors = st.selectbox("**Qualitative**", list(plotly_qualitative.keys()), key="qualitative_colors", index = list(plotly_qualitative.keys()).index("Prism"), help = "Qualitative color palette used when plotting categorical data.")

                    with col2:
                        display_palette_as_gradient(plotly_qualitative[discrete_colors], continuous=False)

                    col3, col4 = st.columns([2, 8], gap="small", vertical_alignment = "center")
                    with col3:
                        continuous_colors = st.selectbox("**Sequential**", list(plotly_sequential.keys()), key="sequential_colors", index = list(plotly_sequential.keys()).index("YlGnBu"), help = "Sequential color palette used when plotting continuous data.")

                    with col4:
                        display_palette_as_gradient(plotly_sequential[continuous_colors])

                    col5, col6 = st.columns([2, 8], gap="small", vertical_alignment = "center")
                    with col5:
                        divergent_colors = st.selectbox("**Diverging**", list(plotly_divergent.keys()), key="diverging_colors", index = list(plotly_divergent.keys()).index("RdBu_r"), help = "Diverging palette used when plotting continuous, centered data.")

                    with col6:
                        display_palette_as_gradient(plotly_divergent[divergent_colors])
    
    # Define color palettes in session state if not already set
    st.session_state.discrete_palette = plotly_qualitative[discrete_colors]
    st.session_state.continuous_palette = ["whitesmoke"] + plotly_sequential[continuous_colors] + ["black"] if add_palette_ends else plotly_sequential[continuous_colors]
    st.session_state.divergent_palette = plotly_divergent[divergent_colors]

    # Initialize the slider value in session state if not already set
    st.session_state.fontsize = fontsize_value

    # Install multipage navigation
    pg = st.navigation(dict(Finances=[p1, p2, p3, p4], Calculators=[p5]))
    pg.run()

if __name__ == "__main__":
    main()
