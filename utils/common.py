import streamlit as st
from utils.pandas_to_polars_functions import pandas_to_polars_transformation_cached
from utils.read_data_functions import read_and_combine_csv_files_pandas_cached
from utils.filtering_functions import filtering_pandas_cached
from utils.aggregation_functions import aggregating_pandas_cached
from utils.join_functions import join_pandas_cached


def clear_cache():
    read_and_combine_csv_files_pandas_cached.clear()
    pandas_to_polars_transformation_cached.clear()
    filtering_pandas_cached.clear()
    aggregating_pandas_cached.clear()
    join_pandas_cached.clear()
