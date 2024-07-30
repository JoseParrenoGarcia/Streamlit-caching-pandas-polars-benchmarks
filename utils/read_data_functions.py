import os
import pandas as pd
import streamlit as st
import time
import polars as pl


def read_and_combine_csv_files_pandas(folder_path):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Initialize an empty list to store DataFrames
    df_list = []

    # Loop through the list of CSV files and read each file into a DataFrame
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df


@st.cache_data()
def read_and_combine_csv_files_pandas_cached(folder_path):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Initialize an empty list to store DataFrames
    df_list = []

    # Loop through the list of CSV files and read each file into a DataFrame
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df


def read_and_combine_csv_files_polars(folder_path):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Initialize an empty list to store DataFrames
    df_list = []

    # Loop through the list of CSV files and read each file into a DataFrame
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pl.read_csv(file_path)
        df_list.append(df)

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pl.concat(df_list)

    return combined_df


def read_data_store_execution_time(dataframes_dict, tag, path, data_format='csv_pandas'):
    # Data format can only be 'csv_pandas', 'csv_pandas_cached', 'csv_polars'

    st.write(tag)
    start_time = time.time()

    if data_format == 'csv_pandas':
        aux_df = read_and_combine_csv_files_pandas(folder_path=path)
    elif data_format == 'csv_pandas_cached':
        aux_df = read_and_combine_csv_files_pandas_cached(folder_path=path)
    elif data_format == 'csv_polars':
        aux_df = read_and_combine_csv_files_polars(folder_path=path)
    else:
        aux_df = read_and_combine_csv_files_pandas(folder_path=path)

    execution_time = time.time() - start_time

    dataframes_dict[tag] = {
        'dataframe': aux_df,
        'execution_time': execution_time
    }

    return dataframes_dict



