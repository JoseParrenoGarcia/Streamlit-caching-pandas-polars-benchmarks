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
st.title('Speed benchmarks for Streamlit caching with Pandas and Polars')

st.write('')
st.html("<b>What</b>")
st.write('This app will try to answer what is the speed of execution for basic operations such as data reads '
         'and data wrangling, depending on the size of the data and the format it is stored.')

st.write('')
st.html("<b>Considerations</b>")
st.write('Of course, things might have changed depending on when you are reading/checking this app. For example,'
         'as of August 2024, I wrote the app based on the following package versions.')

st.markdown("- streamlit==1.35.0 \n"
            "- pandas==2.2.2 \n"
            "- polars==1.3.0 \n"
            )

st.write('')
st.html("<b>Details</b>")
st.write("If you wish to check the exact code which generated this app, feel free to check the GitHub repo"
         "associated with the app.")
st.link_button("GitHub repo", "https://github.com/JoseParrenoGarcia/Streamlit-caching-pandas-polars-benchmarks")