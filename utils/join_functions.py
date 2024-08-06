import pandas as pd
import streamlit as st
import time
import polars as pl
import re


def join_pandas(df: pd.DataFrame, secondary_df: pd.DataFrame = None) -> pd.DataFrame:
    return pd.merge(df, secondary_df, on='Market', how='inner')


@st.cache_data()
def join_pandas_cached(df: pd.DataFrame, secondary_df: pd.DataFrame) -> pd.DataFrame:
    return join_pandas(df, secondary_df)


def join_polars(df: pl.DataFrame, secondary_df: pl.DataFrame) -> pl.DataFrame:
    return df.join(secondary_df, on='Market', how='inner')


def _clean_tag(tag):
    # Remove underscores
    tag = tag.replace('_', ' ')

    # Convert to title case
    tag = tag.title()

    # Handle numbers separately to keep them as they are
    tag = re.sub(r'(\d+)', lambda x: x.group(1), tag)

    return tag


def join_execution_time(loaded_data, dataframes_dict, df_tag, tag, secondary_df, data_format='pandas_filtering',):
    clean_tag = _clean_tag(tag)

    st.write(clean_tag)
    start_time = time.time()

    if data_format == 'pandas':
        aux_df = join_pandas(df=loaded_data[df_tag]['dataframe'], secondary_df=secondary_df)
    elif data_format == 'pandas_cached':
        aux_df = join_pandas_cached(df=loaded_data[df_tag]['dataframe'], secondary_df=secondary_df)
    elif data_format == 'polars':
        aux_df = join_polars(df=loaded_data[df_tag]['dataframe'], secondary_df=secondary_df)
    else:
        aux_df = join_pandas(df=loaded_data[df_tag]['dataframe'])

    execution_time = time.time() - start_time

    dataframes_dict[tag] = {
        'dataframe': aux_df,
        'execution_time': execution_time
    }

    return dataframes_dict
