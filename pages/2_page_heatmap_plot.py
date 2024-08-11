from BankDash import *
import streamlit as st
import plotly.express as px

def main():
    data = st.session_state.data
    fontsize = st.session_state.fontsize
    discrete_palette = st.session_state.discrete_palette
    continuous_palette = st.session_state.continuous_palette
    divergent_palette = st.session_state.divergent_palette
    
    with st.container():
        col1, col2, col3 = st.columns(3, vertical_alignment = "top")
        year_options = data['Year'].unique().astype(int)
        with col1: option_year = st.selectbox('Filter by Year:', year_options, key = "year1", index = len(year_options) - 1)
        filtered_data = data[data["Year"] == option_year]
        with col2: option_focus = st.selectbox("Choose a focus:", ["Sector", "Category", "Group"], key = "focus1", index = 1)
        # Scale data?
        with col3: scale_data = st.radio("Z-Score?", ["No", "Yes"], key = "scale1", horizontal = True)

    p = heatmap_plot(data = filtered_data, scale_data = scale_data, focus = option_focus, continuous_palette = continuous_palette, divergent_palette = divergent_palette, fontsize = fontsize)
    
    st.plotly_chart(p, use_container_width = False)

if __name__ == "__page__":
    main()