import streamlit as st

def render():
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 42px;
                font-weight: 900;
                margin-bottom: -10px;
                background: linear-gradient(90deg, #00c6ff, #0072ff);
                -webkit-background-clip: text;
                color: transparent;
            }
            .subtitle {
                text-align: center;
                font-size: 18px;
                color: #cccccc;
                margin-bottom: 40px;
            }
            .nav-card {
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0px 0px 8px rgba(0,0,0,0.5);
                text-align: center;
                transition: 0.25s;
                cursor: pointer;
            }
            .nav-card:hover {
                transform: scale(1.05);
                background-color: #2a2a2a;
            }
            .nav-card-title {
                font-size: 20px;
                font-weight: 600;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-title'>Data Hunters Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Cross-platform social media analytics for CS 515 &mdash; Project 3</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Row 1
    with col1:
        if st.button(" Activity Trends", key="activity_btn"):
            st.session_state.page = "Activity"
            st.rerun()

    with col2:
        if st.button(" Sentiment Analysis", key="sentiment_btn"):
            st.session_state.page = "Sentiment"
            st.rerun()

    # Row 2
    with col3:
        if st.button(" Toxicity Trends", key="toxicity_btn"):
            st.session_state.page = "Toxicity"
            st.rerun()

    with col4:
        if st.button(" Correlation Explorer", key="correlation_btn"):
            st.session_state.page = "Correlation"
            st.rerun()

    st.write("")
    if st.button("Stock Mentions", key="stocks_btn"):
        st.session_state.page = "Stocks"
        st.rerun()