import polars as pl
import pandas as pd
import streamlit as st


def polars_to_pandas_transformation(df: pl.DataFrame) -> pd.DataFrame:
    return df.to_pandas()


def pandas_to_polars_transformation(df: pd.DataFrame) -> pl.DataFrame:
    return pl.from_pandas(df)


@st.cache_data()
def pandas_to_polars_transformation_cached(df: pd.DataFrame) -> pl.DataFrame:
    return pl.from_pandas(df)
