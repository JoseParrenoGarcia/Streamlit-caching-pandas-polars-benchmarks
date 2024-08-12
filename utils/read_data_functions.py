import os
import pandas as pd
import streamlit as st
import polars as pl
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



