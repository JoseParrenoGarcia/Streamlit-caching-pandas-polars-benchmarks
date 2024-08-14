import pandas as pd
import streamlit as st
import polars as pl
import time

# Fields to sum
sum_fields = ['Impressions', 'Clicks', 'Cost', 'Revenue']

# Fields to average
mean_fields = ['CTR', 'CPC', 'ROI']


def aggregating_pandas(df: pd.DataFrame, list_of_grp_by_fields=None) -> pd.DataFrame:
    start_time = time.time()
    if list_of_grp_by_fields:
        df = (df
              .groupby(list_of_grp_by_fields)
              .agg({**{field: 'sum' for field in sum_fields},
                    **{field: 'mean' for field in mean_fields}}
                   )
              )

        # Rename columns to clarify which operation was performed
        df.columns = [f'{col}_{"Sum" if col in sum_fields else "Avg"}' for col in df.columns]

        # Reset index to make 'Device' and 'Market' regular columns again
        df = df.reset_index()

    execution_time = time.time() - start_time
    print('Pandas aggregation: {}'.format(execution_time))

    return df


@st.cache_data()
def aggregating_pandas_cached(df: pd.DataFrame, list_of_grp_by_fields=None) -> pd.DataFrame:
    start_time = time.time()
    if list_of_grp_by_fields:
        df = (df
              .groupby(list_of_grp_by_fields)
              .agg({**{field: 'sum' for field in sum_fields},
                    **{field: 'mean' for field in mean_fields}}
                   )
              )

        # Rename columns to clarify which operation was performed
        df.columns = [f'{col}_{"Sum" if col in sum_fields else "Avg"}' for col in df.columns]

        # Reset index to make 'Device' and 'Market' regular columns again
        df = df.reset_index()

    execution_time = time.time() - start_time
    print('Pandas cached aggregation: {}'.format(execution_time))

    return df


def aggregating_polars(df: pl.DataFrame, list_of_grp_by_fields=None) -> pl.DataFrame:
    start_time = time.time()
    if list_of_grp_by_fields:
        if 'Date' in list_of_grp_by_fields:
            df = df.with_columns(pl.col('Date').cast(pl.Date))

        agg_exprs = [
            *[pl.col(field).sum().alias(f"{field}_Sum") for field in sum_fields],
            *[pl.col(field).mean().alias(f"{field}_Avg") for field in mean_fields]
        ]

        df = df.group_by(list_of_grp_by_fields).agg(agg_exprs)

    execution_time = time.time() - start_time
    print('Polars aggregation: {}'.format(execution_time))

    return df
