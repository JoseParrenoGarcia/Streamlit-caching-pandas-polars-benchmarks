import pandas as pd
import streamlit as st
import time
import polars as pl
import re
import datetime


def filtering_pandas(df: pd.DataFrame,
                     dates_filter=None,
                     device_filter=None,
                     ROI_filter=None,
                     ) -> pd.DataFrame:

    if dates_filter:
        # Ensure the filter dates are datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        start_date = pd.to_datetime(dates_filter[0])
        end_date = pd.to_datetime(dates_filter[1])
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if device_filter:
        df = df[df['Device'].isin(device_filter)]

    if ROI_filter:
        df = df[(df['ROI'] >= ROI_filter[0]) & (df['ROI'] <= ROI_filter[1])]

    return df


@st.cache_data()
def filtering_pandas_cached(df: pd.DataFrame, dates_filter, device_filter, ROI_filter,) -> pd.DataFrame:
    return filtering_pandas(df, dates_filter, device_filter, ROI_filter)


def filtering_polars(df: pl.DataFrame,
                     dates_filter=None,
                     device_filter=None,
                     ROI_filter=None,
                     ) -> pl.DataFrame:

    if dates_filter:
        # Ensure the filter dates are datetime objects
        df = df.with_columns(pl.col('Date').cast(pl.Date))
        df = df.filter((pl.col('Date') >= dates_filter[0]) & (pl.col('Date') <= dates_filter[1]))

    if device_filter:
        df = df.filter(pl.col('Device').is_in(device_filter))

    if ROI_filter:
        df = df.filter((pl.col('ROI') >= ROI_filter[0]) & (pl.col('ROI') <= ROI_filter[1]))

    return df


def _clean_tag(tag):
    # Remove underscores
    tag = tag.replace('_', ' ')

    # Convert to title case
    tag = tag.title()

    # Handle numbers separately to keep them as they are
    tag = re.sub(r'(\d+)', lambda x: x.group(1), tag)

    return tag


def filtering_execution_time(loaded_data, dataframes_dict, df_tag, tag, dates_filter, device_filter, ROI_filter, data_format='pandas_filtering',):
    clean_tag = _clean_tag(tag)

    st.write(clean_tag)
    start_time = time.time()

    if data_format == 'pandas':
        aux_df = filtering_pandas(df=loaded_data[df_tag]['dataframe'], dates_filter=dates_filter, device_filter=device_filter, ROI_filter=ROI_filter)
    elif data_format == 'pandas_cached':
        aux_df = filtering_pandas_cached(df=loaded_data[df_tag]['dataframe'], dates_filter=dates_filter, device_filter=device_filter, ROI_filter=ROI_filter)
    elif data_format == 'polars':
        aux_df = filtering_polars(df=loaded_data[df_tag]['dataframe'], dates_filter=dates_filter, device_filter=device_filter, ROI_filter=ROI_filter)
    else:
        aux_df = filtering_pandas(df=loaded_data[df_tag]['dataframe'])

    execution_time = time.time() - start_time

    dataframes_dict[tag] = {
        'dataframe': aux_df,
        'execution_time': execution_time
    }

    return dataframes_dict
