import streamlit as st
from pages.pages_format import pages_format
from utils.pandas_to_polars_functions import pd_to_pl_transform_execution_time

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
# datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
datasets = [1_000, 10_000]

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
if 'first_run_execution_time_csv_df' not in st.session_state:
    st.warning('Please navigate to the "Read data" page to load the data')
else:

    loaded_data = st.session_state.loaded_dataframes

    with st.sidebar:
        with st.status("Transforming data...", expanded=True):
            # Dictionary to store execution times of transforming dataframes
            dataframes_dict = {}

            # List of dataset sizes
            for num_rows in datasets:
                df_tag = f'dataframe_{num_rows}_csv_pandas'

                tag = f'dataframe_{num_rows}_pandas_to_polars'
                dataframes_dict = pd_to_pl_transform_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas_to_polars')

                tag = f'dataframe_{num_rows}_pandas_to_polars_cached'
                dataframes_dict = pd_to_pl_transform_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='pandas_to_polars_cached')

                df_tag = f'dataframe_{num_rows}_csv_polars'
                tag = f'dataframe_{num_rows}_polars_to_pandas'
                dataframes_dict = pd_to_pl_transform_execution_time(loaded_data=loaded_data, dataframes_dict=dataframes_dict, df_tag=df_tag, tag=tag, data_format='polars_to_pandas')

            st.success('All data was succesfully transformed!', icon="✅")


# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
if 'first_run_execution_time_csv_df' in st.session_state:
    with st.container(border=True):
        st.html('<h4>Speed of transforming polars to pandas and viceversa</h4>')
        st.write('You might be asking yourself? If I can do everything in Polars, why would I have to transform a dataframe to Pandas? Well nothing comes to mind, but I am'
                 ' sure that as some point, something will come up and I will want to answer this question, so, here we go.')

        st.divider()
        st.write('**For completion, below you can see how the ***st.dataframe()*** method displays the information nicely for both pandas and polars**')
        col1, col2 = st.columns(2)
        with col1:
            st.write('*Streamlit display of polars dataframe*')
            st.dataframe(loaded_data['dataframe_1000_csv_polars']['dataframe'].head(5))

        with col2:
            st.write('*Streamlit display of pandas dataframe*')
            st.dataframe(loaded_data['dataframe_1000_csv_pandas']['dataframe'].head(5))

    st.write(dataframes_dict)
