import streamlit as st
from pages.pages_format import pages_format
from datetime import datetime
import time
from synthetic_data.synthetic_data_generator import datasets, markets
from utils.functools_functions import functools_etl

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
if 'read_data_functools_complete' not in st.session_state:
    st.session_state.read_data_functools_complete = False

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    with st.form('execution_form'):
        st.write('**Aggregate by:**')

        aggregation_fields = st.multiselect('Aggregated by:', options=['Date', 'Device', 'Market'], default=['Device', 'Market'], placeholder='----')
        cumsum_operation = st.checkbox(f'Cumulative sum of clicks ordered by {aggregation_fields[0]}')
        ranking_operation = st.checkbox(f'Ranking of revenue')

        st.divider()

        st.write('**Filter by:**')

        date_filter = st.date_input(label="Date filter:",
                                    value=(datetime(2023, 1, 1), datetime(2024, 12, 31)),
                                    min_value=datetime(2023, 1, 1),
                                    max_value=datetime(2024, 12, 31),
                                    format="YYYY-MM-DD")

        device_filter = st.multiselect('Device:', options=['Desktop', 'Mobile'], placeholder='----')

        market_filter = st.multiselect('Market:', options=markets, placeholder='----')

        ROI_filter = st.slider("ROI", 0.75, 1.55, (0.75, 1.55))

        submitted = st.form_submit_button("Execute", type="primary")

# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
if submitted:
    st.write(date_filter)

    dataframes_dict = {}

    for num_rows in datasets:
        tag = f'dataframe_{num_rows}_csv_pandas_functools'

        start_time = time.time()
        aux_df = functools_etl(folder_path=f'synthetic_data/data_csv/dataset_{num_rows}',
                               dates_filter=date_filter)
        execution_time = time.time() - start_time

        dataframes_dict[tag] = {
            'dataframe': aux_df,
            'execution_time': execution_time
        }


    st.write(dataframes_dict)


