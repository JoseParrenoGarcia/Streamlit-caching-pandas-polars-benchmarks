import pandas as pd
import streamlit as st
import time
import polars as pl
import re

# Fields to sum
sum_fields = ['Impressions', 'Clicks', 'Cost', 'Revenue']

# Fields to average
mean_fields = ['CTR', 'CPC', 'ROI']


def aggregating_pandas(df: pd.DataFrame, list_of_grp_by_fields=None) -> pd.DataFrame:

    if list_of_grp_by_fields:
        df = (df
              .groupby(list_of_grp_by_fields)
              .agg({**{field: 'sum' for field in sum_fields},
                    **{field: 'mean' for field in mean_fields}}
                   )
              )

    return df


@st.cache_data()
def aggregating_pandas_cached(df: pd.DataFrame, list_of_grp_by_fields=None) -> pd.DataFrame:
    return aggregating_pandas(df, list_of_grp_by_fields)


def aggregating_polars(df: pl.DataFrame, list_of_grp_by_fields=None) -> pl.DataFrame:
    if list_of_grp_by_fields:
        agg_exprs = [
            *[pl.col(field).sum().alias(f"{field}_Sum") for field in sum_fields],
            *[pl.col(field).mean().alias(f"{field}_Avg") for field in mean_fields]
        ]

        df = df.group_by(list_of_grp_by_fields).agg(agg_exprs)

    return df
