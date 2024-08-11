import os
import pandas as pd
import streamlit as st
import time
import polars as pl
import re
import functools


def read_and_combine_csv_files_pandas(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    return pd.concat(df_list, ignore_index=True)


@st.cache_data()
def read_and_combine_csv_files_pandas_cached(folder_path):
    return read_and_combine_csv_files_pandas(folder_path)


@functools.lru_cache
def read_and_combine_csv_files_pandas_cached_functools(folder_path):
    return read_and_combine_csv_files_pandas(folder_path)


def read_and_combine_csv_files_polars(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pl.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    return pl.concat(df_list)


@st.cache_data()
def read_and_combine_csv_files_polars_cached(folder_path):
    return read_and_combine_csv_files_polars(folder_path)


def _clean_tag(tag):
    # Remove underscores
    tag = tag.replace('_', ' ')

    # Convert to title case
    tag = tag.title()

    # Handle numbers separately to keep them as they are
    tag = re.sub(r'(\d+)', lambda x: x.group(1), tag)

    return tag


def read_data_store_execution_time(dataframes_dict, tag, path, data_format='csv_pandas'):
    # Data format can only be 'csv_pandas', 'csv_pandas_cached', 'csv_polars', 'csv_polars_cached'

    clean_tag = _clean_tag(tag)

    st.write(clean_tag)
    start_time = time.time()

    if data_format == 'csv_pandas':
        aux_df = read_and_combine_csv_files_pandas(folder_path=path)
    elif data_format == 'csv_pandas_cached':
        aux_df = read_and_combine_csv_files_pandas_cached(folder_path=path)
    elif data_format == 'csv_polars':
        aux_df = read_and_combine_csv_files_polars(folder_path=path)
    elif data_format == 'csv_polars_cached':
        aux_df = read_and_combine_csv_files_polars_cached(folder_path=path)
    elif data_format == 'csv_pandas_functools':
        aux_df = read_and_combine_csv_files_pandas_cached_functools(folder_path=path)
    else:
        aux_df = read_and_combine_csv_files_pandas(folder_path=path)

    execution_time = time.time() - start_time

    dataframes_dict[tag] = {
        'dataframe': aux_df,
        'execution_time': execution_time
    }

    return dataframes_dict



