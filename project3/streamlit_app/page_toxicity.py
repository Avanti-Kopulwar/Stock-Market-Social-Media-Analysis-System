import streamlit as st
from analyses.toxicity import get_toxicity_trends
import plotly.graph_objects as go
import json

def render():
    st.title("Toxicity Trends")

    plots = get_toxicity_trends()

    # Reddit
    st.subheader("Reddit Toxicity")
    reddit_dict = json.loads(plots["reddit_plot"])
    fig_r = go.Figure(reddit_dict)
    st.plotly_chart(fig_r, use_container_width=True)

    # 4chan
    st.subheader("4chan Toxicity")
    chan_dict = json.loads(plots["chan_plot"])
    fig_c = go.Figure(chan_dict)
    st.plotly_chart(fig_c, use_container_width=True)