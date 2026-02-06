import streamlit as st
from analyses.correlation import get_correlation_data

def render():
    st.title("Correlation Explorer")

    # correlation.py returns:
    # reddit_fig, chan_fig, reddit_corr, chan_corr
    reddit_fig, chan_fig, reddit_corr, chan_corr = get_correlation_data()

    st.subheader("Reddit: Sentiment vs Toxicity Correlation")
    st.plotly_chart(reddit_fig, width="stretch")

    st.subheader("/pol/: Sentiment vs Toxicity Correlation")
    st.plotly_chart(chan_fig, width="stretch")

    st.subheader("Correlation Values")
    st.write({
        "Reddit Correlation (r)": reddit_corr,
        "/pol/ Correlation (r)": chan_corr
    })