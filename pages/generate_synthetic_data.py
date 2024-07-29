import streamlit as st
from pages.pages_format import pages_format
from synthetic_data.synthetic_data_generator import generate_dataset


# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)

pages_format()

# ---------------------------------------------------------------------
# INITIALISE SESSION_STATE VARIABLES
# ---------------------------------------------------------------------
if 'synthetic_data_complete' not in st.session_state:
    st.session_state.synthetic_data_complete = False

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    gen_sythn_data_button = st.button("Generate synthetic data", type="primary")

    if st.session_state.synthetic_data_complete is False:
        if gen_sythn_data_button:
            with st.status("Generating synthetic data...", expanded=True):
                # List of dataset sizes
                datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
                for num_rows in datasets:
                    st.write(f"Dataset: {num_rows:,} rows")
                    generate_dataset(num_rows)

            st.session_state.synthetic_data_complete = True

            st.success('Synthetic data generated!', icon="✅")

    else:
        if gen_sythn_data_button:
            st.success('Synthetic data has already been generated.', icon="✅")
            st.write('If you do want to re-generate the data, refresh the page and start again.')

# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
st.html('<h5>Generate synthetic data</h5>')
st.write(' Github does not allow to store data that exceeds 100MB. I wanted to pre-create datasets and stored them in a data'
         ' folder so that this process doesnt have to be re-run every time.')
st.markdown("- Until further resolution, I have decided to create the files on the fly. \n"
            "- You will first have to hit the **Generate synthetic data** button. \n"
            "- This will execute a synthetic data generator and store the data as CSVs and Parquets. \n"
            "- With the data stored, the rest of the pages will be unblocked. \n"
            )

if st.session_state.synthetic_data_complete:
    st.write('hello')



