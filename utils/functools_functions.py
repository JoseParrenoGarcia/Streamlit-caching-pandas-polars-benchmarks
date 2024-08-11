import os
import pandas as pd
import streamlit as st
import time
import re
import functools


@functools.lru_cache
def read_and_combine_csv_files_pandas_cached_functools(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    return pd.concat(df_list, ignore_index=True)


@functools.lru_cache
def filtering_functools(folder_path, dates_filter=None,):
    df = read_and_combine_csv_files_pandas_cached_functools(folder_path)

    if dates_filter:
        # Ensure the filter dates are datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        start_date = pd.to_datetime(dates_filter[0])
        end_date = pd.to_datetime(dates_filter[1])
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    return df


def functools_etl(folder_path, dates_filter=None):
    print('')
    print('----------------------------------------------------------------------------------------')
    print(folder_path)
    print('----------------------------------------------------------------------------------------')
    start_time = time.time()
    df_read = read_and_combine_csv_files_pandas_cached_functools(folder_path)
    execution_time = time.time() - start_time
    print('Read execution time in seconds: {}'.format(execution_time))

    start_time = time.time()
    df_filter = filtering_functools(folder_path=folder_path, dates_filter=dates_filter)
    execution_time = time.time() - start_time
    print('Filter execution time in seconds: {}'.format(execution_time))

    return df_filter
