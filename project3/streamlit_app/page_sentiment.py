import streamlit as st
from analyses.sentiment import get_sentiment_trends

def render():
    st.title("Sentiment Analysis")

    plots = get_sentiment_trends()

    st.subheader("Reddit Sentiment")
    st.plotly_chart(plots["reddit_fig"], use_container_width=True)

    st.subheader("4chan Sentiment (/pol/)")
    st.plotly_chart(plots["chan_fig"], use_container_width=True)