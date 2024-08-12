import pandas as pd
import streamlit as st
import polars as pl


def join_pandas(df: pd.DataFrame, secondary_df: pd.DataFrame = None) -> pd.DataFrame:
    return pd.merge(df, secondary_df, on='Market', how='inner')


@st.cache_data()
def join_pandas_cached(df: pd.DataFrame, secondary_df: pd.DataFrame) -> pd.DataFrame:
    return join_pandas(df, secondary_df)


def join_polars(df: pl.DataFrame, secondary_df: pl.DataFrame) -> pl.DataFrame:
    return df.join(secondary_df, on='Market', how='inner')
