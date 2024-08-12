from BankDash import *
import streamlit as st
import plotly.express as px

def main():
    data = st.session_state.data
    fontsize = st.session_state.fontsize
    continuous_palette = st.session_state.continuous_palette

    p = treemap_plot(data = data, continuous_palette = continuous_palette, fontsize = fontsize)
        
    st.plotly_chart(p, use_container_width = True)

if __name__ == "__page__":
    main()