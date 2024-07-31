import streamlit as st
from pages.pages_format import pages_format
from utils.read_data_functions import read_data_store_execution_time
from utils.plotting_functions import plot_execution_time_bar_charts
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

if 'read_data_first_run_tag' not in st.session_state:
    st.session_state.read_data_first_run_tag = False

if 'first_run_execution_time_csv_df' not in st.session_state:
    st.session_state.first_run_execution_time_csv_df = None

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

                tag = f'dataframe_{num_rows}_csv_polars_cached'
                dataframes_dict = read_data_store_execution_time(dataframes_dict, tag, f'synthetic_data/data_csv/dataset_{num_rows}', data_format='csv_polars_cached')

                st.write('----------------------')

        st.session_state.read_data_complete = True
        st.success('All data was succesfully read!', icon="✅")

        # Extracting the execution times in a dataframe so that we can plot
        execution_time_df = []

        for tag, info in dataframes_dict.items():
            execution_time_df.append({'Tag': tag, 'Execution Time': info['execution_time']})

        execution_time_df = pd.DataFrame(execution_time_df)
        execution_time_df['Number of rows'] = execution_time_df['Tag'].str.extract(r'dataframe_(\d+)')[0].astype(int)
        execution_time_df['Data format'] = execution_time_df['Tag'].str.extract(r'(pandas|pandas_cached|polars|polars_cached)$')[0]

        # Storing the execution_time_df in session state so that we can compare the first run vs following runs
        if st.session_state.read_data_first_run_tag == False:
            st.session_state.first_run_execution_time_csv_df = execution_time_df.copy()

# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
if st.session_state.read_data_complete is False:
    st.warning('Please click on **Read data**')
else:
    with st.container(border=True):
        st.html('<h4>Speed of data reads</h4>')
        st.markdown("- In this page, we will compare how fast do pandas and polars read data \n"
                    "- The data is stored in both CSV and Parquet format. \n"
                    "- In addition, we want to see the effects that ***st.cache_data()*** has on the speed of execution when the app is re-ran. \n"
                    )

    with st.container(border=True):
        st.html('<h5>CSV files</h5>')

        with st.container(border=True):
            st.html('<h6>First run</h6>')
            st.write('Caching doesnt happen the first time you read. Therefore, we dont expect performance differences between the pandas read when its cached or not. '
                     ' The same is expected between cached and not-cached polar reads. In fact, we should see a slightly higher execution time, because (1) first, '
                     ' Streamlit is running the actual function and (2) then it is caching it. The caching operation takes a bit of time, so for the first run, '
                     ' caching is slightly worse. The hope is that this is recovered with caching when the function is re-used by the app.')

            st.plotly_chart(plot_execution_time_bar_charts(st.session_state.first_run_execution_time_csv_df))

        with st.container(border=True):
            st.html('<h6>Second+ run</h6>')
            st.write('If you havent clicked the **Read data** a second time, please do so that caching can take effect...')
            st.write('   ')
            st.write('When you hit **Read data** the second time (or the read functions are used a second time), caching should kick in. We should see a '
                     'difference between the pandas cached vs not cached function. Caching is not supported in polars, so the execution time is not improved with '
                     ' Streamlit caching.')

            st.plotly_chart(plot_execution_time_bar_charts(execution_time_df))

    st.dataframe(execution_time_df)

    st.write(dataframes_dict)
    # st.write(dataframes_dict['dataframe_1000_csv'])
    # st.write(dataframes_dict['dataframe_1000_csv']['dataframe'])
    # st.write(dataframes_dict['dataframe_1000_csv']['execution_time'])
