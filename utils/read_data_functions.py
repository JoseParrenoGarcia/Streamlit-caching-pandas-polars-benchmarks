import os
import pandas as pd
import streamlit as st
import polars as pl
import time


def read_and_combine_csv_files_pandas(folder_path):
    start_time = time.time()
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    return_df = pd.concat(df_list, ignore_index=True)
    execution_time = time.time() - start_time
    print('Pandas read data: {}'.format(execution_time))
    return return_df


@st.cache_data()
def read_and_combine_csv_files_pandas_cached(folder_path):
    start_time = time.time()
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    return_df = pd.concat(df_list, ignore_index=True)
    execution_time = time.time() - start_time
    print('Pandas cached read data: {}'.format(execution_time))
    return return_df


def read_and_combine_csv_files_polars(folder_path):
    start_time = time.time()
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pl.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    return_df = pl.concat(df_list)
    execution_time = time.time() - start_time
    print('Polars read data: {}'.format(execution_time))
    return return_df



