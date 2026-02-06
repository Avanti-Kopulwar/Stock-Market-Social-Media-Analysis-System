import streamlit as st
from analyses.activity import get_activity_trend
import plotly.graph_objects as go

def render():
    st.title("Posting Activity Trends")

    platform = st.selectbox("Select Platform", ["reddit", "chan"])

    if st.button("Generate Chart"):
        fig = get_activity_trend(platform, "2010-01-01", "2030-01-01")

        # fig is already a Plotly Figure object
        st.plotly_chart(fig, use_container_width=True)