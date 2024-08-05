import streamlit as st
from pages.pages_format import pages_format
from datetime import datetime
from utils.common import get_first_run_execution_times, set_first_run_execution_times, clear_cache
from utils.execution_times import execution_times_df, calculate_percent_diff_execution_times
from utils.plotting_functions import plot_execution_time_bar_charts, plot_execution_time_comparison_bar_charts
from synthetic_data.synthetic_data_generator import datasets, markets

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
if 'is_first_run' not in st.session_state:
    st.session_state.is_first_run = True

if 'first_run_execution_time_aggregation_df' not in st.session_state:
    st.session_state.first_run_execution_time_aggregation_df = None

# ---------------------------------------------------------------------
# CACHE FUNCTION TO PERSIST FIRST RUN EXECUTION TIMES
# ---------------------------------------------------------------------
# Clear cache on page refresh (if session state is reset)
if st.session_state.is_first_run:
    clear_cache()
    st.session_state.is_first_run = False

# Load initial execution times from cache if they exist
initial_execution_times = get_first_run_execution_times()

if initial_execution_times is not None:
    st.session_state.first_run_execution_time_filtering_df = initial_execution_times

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
if 'first_run_execution_time_csv_df' not in st.session_state:
    st.warning('Please navigate to the "Read data" page to load the data')
else:
    loaded_data = st.session_state.loaded_dataframes

    with st.sidebar:

        with st.form('aggregation_form'):
            aggregation_fields = st.multiselect('Aggregated by:', options=['Date', 'Device', 'Market'], placeholder='----')

            submitted = st.form_submit_button("Aggregate data (check the field combinations)",  type="primary")

        with st.status("Aggregating data...", expanded=False):
            # Dictionary to store execution times of transforming dataframes
            dataframes_dict = {}

            # List of dataset sizes
            for num_rows in datasets:
                df_tag = f'dataframe_{num_rows}_csv_pandas'
                #
                # tag = f'dataframe_{num_rows}_pandas'
                # dataframes_dict = filtering_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas',
                #                                            dates_filter=date_filter, device_filter=device_filter, ROI_filter=ROI_filter, market_filter=market_filter)
                #
                # tag = f'dataframe_{num_rows}_pandas_cached'
                # dataframes_dict = filtering_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas_cached',
                #                                            dates_filter=date_filter, device_filter=device_filter, ROI_filter=ROI_filter, market_filter=market_filter)
                #
                # df_tag = f'dataframe_{num_rows}_csv_polars'
                # tag = f'dataframe_{num_rows}_polars'
                # dataframes_dict = filtering_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='polars',
                #                                            dates_filter=date_filter, device_filter=device_filter, ROI_filter=ROI_filter, market_filter=market_filter)

        st.success('All data was succesfully filtered!', icon="✅")
