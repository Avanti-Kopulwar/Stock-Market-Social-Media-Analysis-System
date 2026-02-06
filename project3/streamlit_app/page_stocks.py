import streamlit as st
from analyses.stocks import get_stock_mentions

def render():
    st.title("Stock Mentions on Reddit")

    fig = get_stock_mentions()

    if fig is None:
        st.warning("No stock mention data found in the dataset.")
        return

    st.plotly_chart(fig, use_container_width=True)