# import streamlit as st
# from pages.pages_format import pages_format
# from datetime import datetime
# from synthetic_data.synthetic_data_generator import datasets, markets
# from utils.functools_functions import functools_etl
# from utils.execution_times import execution_times_df
# from utils.plotting_functions import plot_execution_time_bar_charts
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
# if 'read_data_functools_complete' not in st.session_state:
#     st.session_state.read_data_functools_complete = False
#
# # ---------------------------------------------------------------------
# # HOME PAGE - SIDEBAR
# # ---------------------------------------------------------------------
# with st.sidebar:
#     with st.form('execution_form'):
#         st.write('**Aggregate by:**')
#
#         aggregation_fields = st.multiselect('Aggregated by:', options=['Date', 'Device', 'Market'], placeholder='----')
#
#         st.divider()
#
#         st.write('**Filter by:**')
#
#         date_filter = st.date_input(label="Date filter:",
#                                     value=(datetime(2023, 1, 1), datetime(2024, 12, 31)),
#                                     min_value=datetime(2023, 1, 1),
#                                     max_value=datetime(2024, 12, 31),
#                                     format="YYYY-MM-DD")
#
#         device_filter = st.multiselect('Device:', options=['Desktop', 'Mobile'], placeholder='----')
#
#         market_filter = st.multiselect('Market:', options=markets, placeholder='----')
#
#         ROI_filter = st.slider("ROI", 0.75, 1.55, (0.75, 1.55))
#
#         submitted = st.form_submit_button("Execute", type="primary")
#
# # ---------------------------------------------------------------------
# # HOME PAGE - MAIN CONTENT AREA
# # ---------------------------------------------------------------------
# if submitted:
#     dataframes_dict = {}
#
#     for num_rows in datasets:
#         dataframes_dict = functools_etl(folder_path=f'synthetic_data/data_csv/dataset_{num_rows}',
#                                num_rows=num_rows,
#                                dataframes_dict=dataframes_dict,
#                                dates_filter=date_filter,
#                                device_filter=device_filter,
#                                market_filter=market_filter,
#                                ROI_filter=ROI_filter,
#                                list_of_grp_by_fields=aggregation_fields,
#                                )
#
#     # Extracting the execution times in a dataframe so that we can plot
#     execution_time_df = execution_times_df(dataframes_dict)
#
#     with st.container(border=True):
#         st.plotly_chart(plot_execution_time_bar_charts(df=execution_time_df,
#                                                        chart_title='How long do different frameworks take?',
#                                                        )
#                         )
#
#
#
