import streamlit as st
from pages.pages_format import pages_format
# from utils.read_data_functions import read_and_combine_csv_files, read_and_combine_csv_files_cached
from utils.read_data_functions import read_data_store_execution_time
import time
import pandas as pd


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
if 'read_data_complete' not in st.session_state:
    st.session_state.read_data_complete = False

datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    read_data_button = st.button("Read data", type="primary")

    if read_data_button:
        with st.status("Reading data...", expanded=True):
            # Dictionary to store DataFrames and its execution time
            dataframes_dict = {}

            # List of dataset sizes
            for num_rows in datasets:
                tag = f'dataframe_{num_rows}_csv_pandas'
                dataframes_dict = read_data_store_execution_time(dataframes_dict, tag, f'synthetic_data/data_csv/dataset_{num_rows}', data_format='csv_pandas')

                tag = f'dataframe_{num_rows}_csv_pandas_cached'
                dataframes_dict = read_data_store_execution_time(dataframes_dict, tag, f'synthetic_data/data_csv/dataset_{num_rows}', data_format='csv_pandas_cached')

                tag = f'dataframe_{num_rows}_csv_polars'
                dataframes_dict = read_data_store_execution_time(dataframes_dict, tag, f'synthetic_data/data_csv/dataset_{num_rows}', data_format='csv_polars')

                st.write('----------------------')

        st.session_state.read_data_complete = True
        st.success('All data was succesfully read!', icon="✅")

        # Extracting the execution times in a dataframe so that we can plot
        execution_time_df = []

        for tag, info in dataframes_dict.items():
            execution_time_df.append({'Tag': tag, 'Execution Time': info['execution_time']})

        execution_time_df = pd.DataFrame(execution_time_df)
        execution_time_df['number_of_rows'] = execution_time_df['Tag'].str.extract(r'dataframe_(\d+)')[0].astype(int)
        execution_time_df['data_format'] = execution_time_df['Tag'].str.extract(r'(csv_pandas|csv_pandas_cached|csv_polars)$')[0]

# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
if st.session_state.read_data_complete is False:
    st.warning('Please click on **Read data**')
else:
    st.html('<h5>Speed of data reads</h5>')
    st.write('In this page, we will compare how fast do pandas and polars read data. In addition, we want to see the effects that <i>st.cache_data()</i> has on'
             ' the speed of execution when the app is re-ran.')

    st.dataframe(execution_time_df)

    st.write(dataframes_dict)
    # st.write(dataframes_dict['dataframe_1000_csv'])
    # st.write(dataframes_dict['dataframe_1000_csv']['dataframe'])
    # st.write(dataframes_dict['dataframe_1000_csv']['execution_time'])



