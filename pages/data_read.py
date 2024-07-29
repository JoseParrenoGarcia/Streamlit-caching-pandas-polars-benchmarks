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
# DATA READ EXECUTION
# ---------------------------------------------------------------------
datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]



# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    st.write('hello2')

# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
st.html('<h5>Speed of data reads</h5>')
st.write('In this page, we will compare how fast do pandas and polars read data. In addition, we want to see the effects that <i>st.cache_data()</i> has on'
         ' the speed of execution when the app is re-ran.')
st.markdown("- Unfortunately, Github does not allow to store data that exceeds 100MB. \n"
            "- For datasets of 1m+ records, we would be hitting this limit. \n"
            "- Until further resolution, I have decided to create the files on the fly. \n"
            "- In other words, the execution of the app might be slower because we have to run the synthetic generator code for big datasets. \n"
            )

