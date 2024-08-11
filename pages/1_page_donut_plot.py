from BankDash import *
import streamlit as st
import plotly.express as px


def main():
    data = st.session_state.data
    fontsize = st.session_state.fontsize
    discrete_palette = st.session_state.discrete_palette
    
    
    col1, col2 = st.columns([2, 8])

    with st.container():
        col1, col2, col3, col4 = st.columns(4, vertical_alignment = "top")


        year_options = data['Year'].unique().astype(int)
        with col1: option_year = st.radio('Filter by Year:', year_options, key = "year1", index = len(year_options) - 1)
        filtered_data = data[data["Year"] == option_year]
        with col2: option_focus = st.radio("Choose a focus:", ["Sector", "Category", "Group"], key = "focus1", index = 1)

        # Pie options.
        with col3: option_subset = st.selectbox("Choose a Subset:", ["None"] + sorted(data[option_focus].dropna().unique().tolist()), key="subset1")
        with col4: option_month = st.selectbox("Choose a Month:", ["All months"] + data[data["Year"] == option_year]["Month"].dropna().unique().tolist())
        
      
    p = donut_plot(data = filtered_data, 
                   year = option_year,
                   month = option_month,
                   focus = option_focus,
                   subset = option_subset,
                   discrete_palette = discrete_palette, 
                   fontsize = fontsize)
    st.plotly_chart(p, use_container_width = True)

if __name__ == "__page__":
    main()