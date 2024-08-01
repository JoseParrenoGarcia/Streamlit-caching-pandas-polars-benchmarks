import polars as pl
import pandas as pd
import time
import streamlit as st
import re


def polars_to_pandas_transformation(df: pl.DataFrame) -> pd.DataFrame:
    return df.to_pandas()


def pandas_to_polars_transformation(df: pd.DataFrame) -> pl.DataFrame:
    return pl.from_pandas(df)


@st.cache_data()
def pandas_to_polars_transformation_cached(df: pd.DataFrame) -> pl.DataFrame:
    return pl.from_pandas(df)

def _clean_tag(tag):
    # Remove underscores
    tag = tag.replace('_', ' ')

    # Convert to title case
    tag = tag.title()

    # Handle numbers separately to keep them as they are
    tag = re.sub(r'(\d+)', lambda x: x.group(1), tag)

    return tag


def pd_to_pl_transform_execution_time(loaded_data, dataframes_dict, df_tag, tag, data_format='pandas_to_polars'):
    clean_tag = _clean_tag(tag)

    st.write(clean_tag)
    start_time = time.time()

    if data_format == 'pandas_to_polars':
        aux_df = pandas_to_polars_transformation(df=loaded_data[df_tag]['dataframe'])
    elif data_format == 'pandas_to_polars_cached':
        aux_df = pandas_to_polars_transformation_cached(df=loaded_data[df_tag]['dataframe'])
    elif data_format == 'polars_to_pandas':
        aux_df = polars_to_pandas_transformation(df=loaded_data[df_tag]['dataframe'])
    else:
        aux_df = pandas_to_polars_transformation(df=loaded_data[df_tag]['dataframe'])

    execution_time = time.time() - start_time

    dataframes_dict[tag] = {
        'execution_time': execution_time
    }

    return dataframes_dict
