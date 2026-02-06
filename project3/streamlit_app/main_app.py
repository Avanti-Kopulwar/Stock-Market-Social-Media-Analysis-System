import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st

import page_home
import page_activity
import page_sentiment
import page_toxicity
import page_correlation
import page_stocks

st.set_page_config(page_title="Data Hunters Dashboard", layout="wide")


st.markdown("""
<style>

.stock-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 250%;
    height: 100%;
    opacity: 0.20;                     /* Bright enough to see */
    color: #00ffcc;                    /* Neon turquoise */
    font-size: 32px;                   /* Big ticker text */
    font-weight: 600;
    font-family: monospace;
    animation: scrollTicker 12s linear infinite;
    white-space: nowrap;
    pointer-events: none;
    z-index: -1;
    text-shadow: 0px 0px 8px #00ffaa;   /* Glow effect */
}

@keyframes scrollTicker {
    from { transform: translateX(0); }
    to   { transform: translateX(-60%); }
}

/* Add a soft dark overlay for readability */
body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.45);
    z-index: -2;
}

</style>

<div class="stock-bg">
    AAPL ↑ TSLA ↓ MSFT ↑ NVDA ↑ META ↑ GOOGL ↓ AMD ↑ AMZN ↑ BTC ↑ ETH ↑ SPY ↑ QQQ ↑ 
    AAPL ↑ TSLA ↓ MSFT ↑ NVDA ↑ META ↑ GOOGL ↓ AMD ↑ AMZN ↑ BTC ↑ ETH ↑ SPY ↑ QQQ ↑
    AAPL ↑ TSLA ↓ MSFT ↑ NVDA ↑ META ↑ GOOGL ↓ AMD ↑ AMZN ↑ BTC ↑ ETH ↑ SPY ↑ QQQ ↑
</div>
""", unsafe_allow_html=True)



if "page" not in st.session_state:
    st.session_state.page = "Home"



with st.sidebar:
    st.title("Navigation")
    if st.button("Home"):
        st.session_state.page = "Home"
    if st.button("Activity"):
        st.session_state.page = "Activity"
    if st.button("Sentiment"):
        st.session_state.page = "Sentiment"
    if st.button("Toxicity"):
        st.session_state.page = "Toxicity"
    if st.button("Correlation"):
        st.session_state.page = "Correlation"
    if st.button("Stocks"):
        st.session_state.page = "Stocks"


page = st.session_state.page

if page == "Home":
    page_home.render()
elif page == "Activity":
    page_activity.render()
elif page == "Sentiment":
    page_sentiment.render()
elif page == "Toxicity":
    page_toxicity.render()
elif page == "Correlation":
    page_correlation.render()
elif page == "Stocks":
    page_stocks.render()