from BankDash import *
import streamlit as st
import plotly.express as px

def main():
    data = st.session_state.data
    fontsize = st.session_state.fontsize
    discrete_palette_2 = st.session_state.discrete_palette_2

    with st.container():
        col1, col2, col3 = st.columns(3)
        year_options = data['Year'].unique().astype(int)
        with col1: years = st.selectbox('Filter by Year:', year_options, key = "year2", index = len(year_options) - 1)
        with col2: focus = st.selectbox("Select a Focus", options =  ["Sector", "Category", "Group"])
        

    filtered_data = data[data["Year"] == years]

    p = scatter_plot(data = filtered_data, focus = focus, discrete_palette = discrete_palette_2, fontsize = fontsize)

    st.plotly_chart(p, use_container_width = True)

if __name__ == "__page__":
    main()