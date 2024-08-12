# import streamlit as st
# from pages.pages_format import pages_format
# from utils.common import get_first_run_execution_times, set_first_run_execution_times, clear_cache
# from utils.join_functions import join_execution_time
# from utils.execution_times import execution_times_df, calculate_percent_diff_execution_times
# from utils.plotting_functions import plot_execution_time_bar_charts, plot_execution_time_comparison_bar_charts
# from synthetic_data.synthetic_data_generator import datasets, markets
# import pandas as pd
# import polars as pl
#
# # ---------------------------------------------------------------------
# # HOME PAGE - CONFIGURATION
# # ---------------------------------------------------------------------
# st.set_page_config(
#     layout="wide",
# )
#
# pages_format()
#
# # ---------------------------------------------------------------------
# # INITIALISE SESSION_STATE VARIABLES
# # ---------------------------------------------------------------------
# if 'is_first_run' not in st.session_state:
#     st.session_state.is_first_run = True
#
# if 'first_run_execution_time_join_df' not in st.session_state:
#     st.session_state.first_run_execution_time_join_df = None
#
# # ---------------------------------------------------------------------
# # CACHE FUNCTION TO PERSIST FIRST RUN EXECUTION TIMES
# # ---------------------------------------------------------------------
# # Clear cache on page refresh (if session state is reset)
# if st.session_state.is_first_run:
#     clear_cache()
#     st.session_state.is_first_run = False
#
# # Load initial execution times from cache if they exist
# initial_execution_times = get_first_run_execution_times()
#
# if initial_execution_times is not None:
#     st.session_state.first_run_execution_time_join_df = initial_execution_times
#
# # ---------------------------------------------------------------------
# # HOME PAGE - SIDEBAR
# # ---------------------------------------------------------------------
# if 'first_run_execution_time_csv_df' not in st.session_state:
#     st.warning('Please navigate to the "Read data" page to load the data')
# else:
#     loaded_data = st.session_state.loaded_dataframes
#
#     with st.sidebar:
#         with st.status("Joining data...", expanded=False):
#             # Read secondary data
#             markets_pandas_df = pd.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')
#             markets_polars_df = pl.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')
#
#             # Dictionary to store execution times of transforming dataframes
#             dataframes_dict = {}
#
#             # List of dataset sizes
#             for num_rows in datasets:
#                 df_tag = f'dataframe_{num_rows}_csv_pandas'
#
#                 tag = f'dataframe_{num_rows}_pandas'
#                 dataframes_dict = join_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas',
#                                                       secondary_df=markets_pandas_df)
#
#                 tag = f'dataframe_{num_rows}_pandas_cached'
#                 dataframes_dict = join_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas_cached',
#                                                       secondary_df=markets_pandas_df)
#
#                 df_tag = f'dataframe_{num_rows}_csv_polars'
#                 tag = f'dataframe_{num_rows}_polars'
#                 dataframes_dict = join_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='polars',
#                                                       secondary_df=markets_polars_df)
#
#         st.success('All data was succesfully filtered!', icon="✅")
#
#         # Extracting the execution times in a dataframe so that we can plot
#         execution_time_df = execution_times_df(dataframes_dict)
#
#         # # Storing the execution_time_df in session state so that we can compare the first run vs following runs
#         # if st.session_state.first_run_execution_time_join_df is None:
#         #     st.session_state.first_run_execution_time_join_df = execution_time_df.copy()
#         #     set_first_run_execution_times(execution_time_df)
#
#         comparison_baseline_radio = st.radio(label='Compare execution times against:',
#                                              options=execution_time_df['Data format'].unique())
#
#         st.divider()
#
#         read_data_button = st.button("Join data for second+ time", type="primary")
#
# # ---------------------------------------------------------------------
# # HOME PAGE - MAIN CONTENT AREA
# # ---------------------------------------------------------------------
# if 'first_run_execution_time_csv_df' in st.session_state:
#     with st.container(border=True):
#         st.html('<h4>Speed of joining data in pandas, cached pandas and polars</h4>')
#
#         st.write('**Dataframe after aggregating**')
#         with st.expander('Pandas dataframe', expanded=False):
#             st.dataframe(dataframes_dict['dataframe_1000_pandas']['dataframe'])
#
#         with st.expander('Polars dataframe', expanded=False):
#             st.dataframe(dataframes_dict['dataframe_1000_polars']['dataframe'])
#
#
#     with st.container(border=True):
#         st.html('<h5>Comparing execution times</h5>')
#
#         with st.container(border=True):
#             st.plotly_chart(plot_execution_time_bar_charts(df=execution_time_df,
#                                                            chart_title='Join speed',
#                                                            )
#                             )
#
#         with st.container(border=True):
#             diffs_cached = calculate_percent_diff_execution_times(execution_time_df=execution_time_df,
#                                                                   selected_baseline=comparison_baseline_radio
#                                                                   )
#
#             st.plotly_chart(plot_execution_time_comparison_bar_charts(df=diffs_cached,
#                                                                       selected_baseline=comparison_baseline_radio,
#                                                                       chart_title=f'How much faster is joining vs using {comparison_baseline_radio}?',
#                                                                       )
#                             )
#
#
