import pandas as pd
import streamlit as st
import polars as pl
import time


def filtering_pandas(df: pd.DataFrame,
                     dates_filter=None,
                     device_filter=None,
                     ROI_filter=None,
                     market_filter=None
                     ) -> pd.DataFrame:
    start_time = time.time()

    if dates_filter:
        # Ensure the filter dates are datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        start_date = pd.to_datetime(dates_filter[0])
        end_date = pd.to_datetime(dates_filter[1])
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if device_filter:
        df = df[df['Device'].isin(device_filter)]

    if market_filter:
        df = df[df['Market'].isin(market_filter)]

    if ROI_filter:
        df = df[(df['ROI'] >= ROI_filter[0]) & (df['ROI'] <= ROI_filter[1])]

    execution_time = time.time() - start_time
    print('Pandas filter: {}'.format(execution_time))

    return df


@st.cache_data()
def filtering_pandas_cached(df: pd.DataFrame, dates_filter, device_filter, ROI_filter, market_filter) -> pd.DataFrame:
    start_time = time.time()
    if dates_filter:
        # Ensure the filter dates are datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        start_date = pd.to_datetime(dates_filter[0])
        end_date = pd.to_datetime(dates_filter[1])
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if device_filter:
        df = df[df['Device'].isin(device_filter)]

    if market_filter:
        df = df[df['Market'].isin(market_filter)]

    if ROI_filter:
        df = df[(df['ROI'] >= ROI_filter[0]) & (df['ROI'] <= ROI_filter[1])]

    execution_time = time.time() - start_time
    print('Pandas cached filter: {}'.format(execution_time))

    return df


def filtering_polars(df: pl.DataFrame,
                     dates_filter=None,
                     device_filter=None,
                     ROI_filter=None,
                     market_filter=None
                     ) -> pl.DataFrame:
    start_time = time.time()

    if dates_filter:
        # Ensure the filter dates are datetime objects
        df = df.with_columns(pl.col('Date').cast(pl.Date))
        df = df.filter((pl.col('Date') >= dates_filter[0]) & (pl.col('Date') <= dates_filter[1]))

    if device_filter:
        df = df.filter(pl.col('Device').is_in(device_filter))

    if market_filter:
        df = df.filter(pl.col('Market').is_in(market_filter))

    if ROI_filter:
        df = df.filter((pl.col('ROI') >= ROI_filter[0]) & (pl.col('ROI') <= ROI_filter[1]))

    execution_time = time.time() - start_time
    print('Polars filter: {}'.format(execution_time))

    return df
