import streamlit as st
from pages.pages_format import pages_format


# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)

pages_format()

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    st.write(' ')

# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
st.html('<h5>Speed of data reads</h5>')
st.write('In this page, we will compare how fast do pandas and polars read data. In addition, we want to see the effects that <i>st.cache_data()</i> has on'
         ' the speed of execution when the app is re-ran.')



