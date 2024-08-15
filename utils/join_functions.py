import pandas as pd
import streamlit as st
import polars as pl
import time


def join_pandas(df: pd.DataFrame, secondary_df: pd.DataFrame = None) -> pd.DataFrame:
    start_time = time.time()
    return_df = pd.merge(df, secondary_df, on='Market', how='inner')
    execution_time = time.time() - start_time
    print('Pandas join: {}'.format(execution_time))

    return return_df


@st.cache_data()
def join_pandas_cached(df: pd.DataFrame, secondary_df: pd.DataFrame) -> pd.DataFrame:
    start_time = time.time()
    return_df = pd.merge(df, secondary_df, on='Market', how='inner')
    execution_time = time.time() - start_time
    print('Pandas cached join: {}'.format(execution_time))
    return return_df


def join_polars(df: pl.DataFrame, secondary_df: pl.DataFrame) -> pl.DataFrame:
    start_time = time.time()
    return_df = df.join(secondary_df, on='Market', how='inner')
    execution_time = time.time() - start_time
    print('Polars join: {}'.format(execution_time))
    return return_df
