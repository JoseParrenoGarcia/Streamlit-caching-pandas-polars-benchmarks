import streamlit as st
from pages.pages_format import pages_format
import numpy as np
from datetime import datetime
from synthetic_data.synthetic_data_generator import markets
from utils.comparison_etl import etl_comparisons
from utils.plotting_functions import plot_execution_time_bar_charts, plot_execution_time_comparison_bar_charts
from utils.execution_times import execution_times_df, calculate_percent_diff_execution_times
from utils.common import clear_cache
from synthetic_data.synthetic_data_generator import datasets

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

# if 'loaded_dataframes' not in st.session_state:
#     st.session_state.loaded_dataframes = None

if 'is_first_run' not in st.session_state:
    st.session_state.is_first_run = True


# ---------------------------------------------------------------------
# CACHE FUNCTION TO PERSIST FIRST RUN EXECUTION TIMES
# ---------------------------------------------------------------------
# Clear cache on page refresh (if session state is reset)
if st.session_state.is_first_run:
    clear_cache()
    st.session_state.is_first_run = False

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    with st.form('execution_form'):
        st.write('**Aggregate by:**')

        aggregation_fields = st.multiselect('Aggregated by:', options=['Date', 'Device', 'Market'], placeholder='----')

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
    dataframes_dict = {}

    for num_rows in datasets:
        dataframes_dict = etl_comparisons(folder_path=f'synthetic_data/data_csv/dataset_{num_rows}',
                                          num_rows=num_rows,
                                          dataframes_dict=dataframes_dict,
                                          dates_filter=date_filter,
                                          device_filter=device_filter,
                                          market_filter=market_filter,
                                          ROI_filter=ROI_filter,
                                          list_of_grp_by_fields=aggregation_fields,
                                          )

    # Extracting the execution times in a dataframe so that we can plot
    execution_time_df = execution_times_df(dataframes_dict)

    # with st.container(border=True):
    #     with st.expander('Pandas dataframe', expanded=False):
    #         st.dataframe(dataframes_dict['dataframe_1000_csv_pandas']['dataframe'], hide_index=True)
    #
    #     with st.expander('Pandas streamlit cached dataframe', expanded=False):
    #         st.dataframe(dataframes_dict['dataframe_1000_csv_pandas_streamlit_cached']['dataframe'], hide_index=True)
    #
    #     with st.expander('Pandas functools cached dataframe', expanded=False):
    #         st.dataframe(dataframes_dict['dataframe_1000_csv_pandas_functools_cached']['dataframe'], hide_index=True)
    #
    #     with st.expander('Polars dataframe', expanded=False):
    #         st.dataframe(dataframes_dict['dataframe_1000_csv_polars']['dataframe'], hide_index=True)
    #
    #     with st.expander('Polars functools cached dataframe', expanded=False):
    #         st.dataframe(dataframes_dict['dataframe_1000_csv_polars_functools_cached']['dataframe'], hide_index=True)

    with st.container(border=True):
        st.plotly_chart(plot_execution_time_bar_charts(df=execution_time_df,
                                                       chart_title='',
                                                       )
                        )

    with st.container(border=True):
        # comparison_baseline_radio = st.radio(label='Compare execution times against:',
        #                                      options=np.sort(execution_time_df['Data format'].unique()),
        #                                      horizontal=True)
        comparison_baseline_radio = 'pandas'

        diffs_cached = calculate_percent_diff_execution_times(execution_time_df=execution_time_df,
                                                              selected_baseline=comparison_baseline_radio
                                                              )

        st.plotly_chart(plot_execution_time_comparison_bar_charts(df=diffs_cached,
                                                                  selected_baseline=comparison_baseline_radio,
                                                                  chart_title=f'How much faster is reading vs using {comparison_baseline_radio}?',
                                                                  )
                        )


