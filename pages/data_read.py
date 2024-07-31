import streamlit as st
from pages.pages_format import pages_format
from utils.read_data_functions import read_data_store_execution_time, read_and_combine_csv_files_polars_cached, read_and_combine_csv_files_pandas_cached
from utils.plotting_functions import plot_execution_time_bar_charts, plot_execution_time_comparison_bar_charts
from utils.execution_times import execution_times_df, calculate_percent_diff_execution_times

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

if 'first_run_execution_time_csv_df' not in st.session_state:
    st.session_state.first_run_execution_time_csv_df = None

if 'loaded_dataframes' not in st.session_state:
    st.session_state.loaded_dataframes = None

if 'is_first_run' not in st.session_state:
    st.session_state.is_first_run = True

datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]


# ---------------------------------------------------------------------
# CACHE FUNCTION TO PERSIST FIRST RUN EXECUTION TIMES
# ---------------------------------------------------------------------
def get_first_run_execution_times():
    return None


@st.cache_data
def set_first_run_execution_times(df):
    return df

def clear_cache():
    read_and_combine_csv_files_pandas_cached.clear()
    read_and_combine_csv_files_polars_cached.clear()


# Clear cache on page refresh (if session state is reset)
if st.session_state.is_first_run:
    clear_cache()
    st.session_state.is_first_run = False

# Load initial execution times from cache if they exist
initial_execution_times = get_first_run_execution_times()

if initial_execution_times is not None:
    st.session_state.first_run_execution_time_csv_df = initial_execution_times

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    with st.status("Reading data...", expanded=False):
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
    execution_time_df = execution_times_df(dataframes_dict)

    # Storing the execution_time_df in session state so that we can compare the first run vs following runs
    if st.session_state.first_run_execution_time_csv_df is None:
        st.session_state.first_run_execution_time_csv_df = execution_time_df.copy()
        st.session_state.loaded_dataframes = dataframes_dict
        set_first_run_execution_times(execution_time_df)

    comparison_baseline_radio = st.radio(label='Compare execution times against:',
                                         options=execution_time_df['Data format'].unique())

    st.divider()

    read_data_button = st.button("Read data for second+ time", type="primary")

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

            col1, col2 = st.columns([1.5, 1])

            with col1:
                with st.container(border=True):
                    st.plotly_chart(plot_execution_time_bar_charts(df=st.session_state.first_run_execution_time_csv_df,
                                                                   chart_title='How long do different frameworks take to read different volumes of rows?',
                                                                   )
                                    )

            with col2:
                with st.container(border=True):
                    diffs = calculate_percent_diff_execution_times(execution_time_df=st.session_state.first_run_execution_time_csv_df,
                                                                   selected_baseline=comparison_baseline_radio
                                                                   )

                    st.plotly_chart(plot_execution_time_comparison_bar_charts(df=diffs,
                                                                              selected_baseline=comparison_baseline_radio,
                                                                              chart_title=f'How much faster is reading vs using {comparison_baseline_radio}?',
                                                                              )
                                    )

        with st.container(border=True):
            st.html('<h6>Second+ run</h6>')
            st.write('If you havent clicked the **Read data** a second time, please do so that caching can take effect...')
            st.write('   ')
            st.write('When you hit **Read data** the second time (or the read functions are used a second time), caching should kick in. We should see a '
                     'difference between the pandas cached vs not cached function. Caching is not supported in polars, so the execution time is not improved with '
                     ' Streamlit caching.')

            col1, col2 = st.columns([1.5, 1])

            with col1:
                with st.container(border=True):
                    st.plotly_chart(plot_execution_time_bar_charts(df=execution_time_df,
                                                                   chart_title='How long do different frameworks take to read different volumes of rows?',
                                                                   )
                                    )

            with col2:
                with st.container(border=True):
                    diffs_cached = calculate_percent_diff_execution_times(execution_time_df=execution_time_df,
                                                                          selected_baseline=comparison_baseline_radio
                                                                          )

                    st.plotly_chart(plot_execution_time_comparison_bar_charts(df=diffs_cached,
                                                                              selected_baseline=comparison_baseline_radio,
                                                                              chart_title=f'How much faster is reading vs using {comparison_baseline_radio}?',
                                                                              )
                                    )
