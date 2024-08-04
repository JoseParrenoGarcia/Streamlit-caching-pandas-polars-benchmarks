import streamlit as st
from pages.pages_format import pages_format
from datetime import datetime
from utils.common import get_first_run_execution_times, set_first_run_execution_times, clear_cache
from utils.filtering_functions import filtering_execution_time
from utils.execution_times import execution_times_df, calculate_percent_diff_execution_times
from utils.plotting_functions import plot_execution_time_bar_charts, plot_execution_time_comparison_bar_charts

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

if 'first_run_execution_time_filtering_df' not in st.session_state:
    st.session_state.first_run_execution_time_filtering_df = None

datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]


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

        with st.form('filtering_form'):
            date_filter = st.date_input(label="Date filter:",
                                        value=(datetime(2023, 1, 1), datetime(2024, 12, 31)),
                                        min_value=datetime(2023, 1, 1),
                                        max_value=datetime(2024, 12, 31),
                                        format="YYYY-MM-DD")

            device_filter = st.multiselect('Device:', options=['Desktop', 'Mobile'], placeholder='----')

            ROI_filter = st.slider("ROI", 0.75, 1.55, (0.75, 1.55))

            submitted = st.form_submit_button("Filter data (check the filter combinations)",  type="primary")
            if submitted:
                st.write("date", date_filter, "checkbox", device_filter, 'slider', ROI_filter)

        with st.status("Filtering data...", expanded=False):
            # Dictionary to store execution times of transforming dataframes
            dataframes_dict = {}

            # List of dataset sizes
            for num_rows in datasets:
                df_tag = f'dataframe_{num_rows}_csv_pandas'

                tag = f'dataframe_{num_rows}_pandas'
                dataframes_dict = filtering_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas',
                                                           dates_filter=date_filter, device_filter=device_filter, ROI_filter=ROI_filter)

                tag = f'dataframe_{num_rows}_pandas_cached'
                dataframes_dict = filtering_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas_cached',
                                                           dates_filter=date_filter, device_filter=device_filter, ROI_filter=ROI_filter)

                df_tag = f'dataframe_{num_rows}_csv_polars'
                tag = f'dataframe_{num_rows}_polars'
                dataframes_dict = filtering_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='polars',
                                                           dates_filter=date_filter, device_filter=device_filter, ROI_filter=ROI_filter)

        st.success('All data was succesfully filtered!', icon="✅")

        # Extracting the execution times in a dataframe so that we can plot
        execution_time_df = execution_times_df(dataframes_dict)

        # Storing the execution_time_df in session state so that we can compare the first run vs following runs
        if st.session_state.first_run_execution_time_filtering_df is None:
            st.session_state.first_run_execution_time_filtering_df = execution_time_df.copy()
            set_first_run_execution_times(execution_time_df)

        comparison_baseline_radio = st.radio(label='Compare execution times against:',
                                             options=execution_time_df['Data format'].unique())

        st.divider()


# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
if 'first_run_execution_time_csv_df' in st.session_state:
    with st.container(border=True):
        st.html('<h4>Speed of filtering data in pandas, cached pandas and polars</h4>')
        st.write('talk about caching specific inputs')
        st.write(execution_time_df)
        st.write(dataframes_dict['dataframe_1000_pandas'])
        # st.write(loaded_data)

    with st.container(border=True):
        st.html('<h5>Comparing execution times</h5>')

        with st.container(border=True):
            st.html('<h6>First run - <i>no caching</i></h6>')

            col1, col2 = st.columns([1.5, 1])

            with col1:
                with st.container(border=True):
                    st.write('hello')
                    # st.plotly_chart(plot_execution_time_bar_charts(df=st.session_state.first_run_execution_time_pd_to_pl_df,
                    #                                                chart_title='How fast is the conversion between frameworks?',
                    #                                                )
                    #                 )

            with col2:
                with st.container(border=True):
                    st.write('hello')
                    # diffs = calculate_percent_diff_execution_times(execution_time_df=st.session_state.first_run_execution_time_pd_to_pl_df,
                    #                                                selected_baseline=comparison_baseline_radio
                    #                                                )
                    #
                    # st.plotly_chart(plot_execution_time_comparison_bar_charts(df=diffs,
                    #                                                           selected_baseline=comparison_baseline_radio,
                    #                                                           chart_title=f'How much faster is conversion vs using {comparison_baseline_radio}?',
                    #                                                           )
                    #                 )

        with st.container(border=True):
            st.html('<h6>Second+ run</h6>')
            st.write('If you havent clicked the **XXX** a second time, please do so that caching can take effect...')
            st.write('   ')
            st.write('When you hit **XXX** the second time (or the read functions are used a second time), caching should kick in. '
                     'We have added a cached function to transform pandas to polars. We havent been able to add a cached one when we wanted to transform polars to pandas. '
                     'This is because polars is not an accepted format to cache. Nevertheless, we will compare execution times of polars to pandas, and pandas to polars (cached '
                     'and not cached)')

            col1, col2 = st.columns([1.5, 1])

            with col1:
                with st.container(border=True):
                    st.write('hello')
                    # st.plotly_chart(plot_execution_time_bar_charts(df=execution_time_df,
                    #                                                chart_title='How fast is the conversion between frameworks?',
                    #                                                )
                    #                 )

            with col2:
                with st.container(border=True):
                    st.write('hello')
                    # diffs_cached = calculate_percent_diff_execution_times(execution_time_df=execution_time_df,
                    #                                                       selected_baseline=comparison_baseline_radio
                    #                                                       )
                    #
                    # st.plotly_chart(plot_execution_time_comparison_bar_charts(df=diffs_cached,
                    #                                                           selected_baseline=comparison_baseline_radio,
                    #                                                           chart_title=f'How much faster is conversion vs using {comparison_baseline_radio}?',
                    #                                                           )
                    #                 )

