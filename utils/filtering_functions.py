import pandas as pd
import streamlit as st
import time
import polars as pl
import re


def filtering_pandas(df: pd.DataFrame,
                     dates_filter=None,
                     device_filter=None,
                     ROI_filter=None,
                     ) -> pd.DataFrame:

    if dates_filter:
        # Ensure the filter dates are datetime objects
        start_date = pd.to_datetime(dates_filter[0])
        end_date = pd.to_datetime(dates_filter[1])
        df = df[(df['dt'] >= start_date) & (df['dt'] <= end_date)]

    return df


@st.cache_data()
def filtering_pandas_cached(df: pd.DataFrame) -> pd.DataFrame:
    return filtering_pandas(df)


def filtering_polars(df: pl.DataFrame) -> pl.DataFrame:
    return df


def _clean_tag(tag):
    # Remove underscores
    tag = tag.replace('_', ' ')

    # Convert to title case
    tag = tag.title()

    # Handle numbers separately to keep them as they are
    tag = re.sub(r'(\d+)', lambda x: x.group(1), tag)

    return tag


def filtering_execution_time(loaded_data, dataframes_dict, df_tag, tag, data_format='pandas_filtering'):
    clean_tag = _clean_tag(tag)

    st.write(clean_tag)
    start_time = time.time()

    if data_format == 'pandas':
        aux_df = filtering_pandas(df=loaded_data[df_tag]['dataframe'])
    elif data_format == 'pandas_cached':
        aux_df = filtering_pandas_cached(df=loaded_data[df_tag]['dataframe'])
    elif data_format == 'polars':
        aux_df = filtering_polars(df=loaded_data[df_tag]['dataframe'])
    else:
        aux_df = filtering_pandas(df=loaded_data[df_tag]['dataframe'])

    execution_time = time.time() - start_time

    dataframes_dict[tag] = {
        'execution_time': execution_time
    }

    return dataframes_dict
