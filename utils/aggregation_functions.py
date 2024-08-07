import pandas as pd
import streamlit as st
import time
import polars as pl
import re

# Fields to sum
sum_fields = ['Impressions', 'Clicks', 'Cost', 'Revenue']

# Fields to average
mean_fields = ['CTR', 'CPC', 'ROI']


def aggregating_pandas(df: pd.DataFrame,
                       list_of_grp_by_fields=None,
                       cumsum_operation=None,
                       ranking_operation=None,
                       ) -> pd.DataFrame:

    if list_of_grp_by_fields:
        df = (df
              .groupby(list_of_grp_by_fields)
              .agg({**{field: 'sum' for field in sum_fields},
                    **{field: 'mean' for field in mean_fields}}
                   )
              )

        # Rename columns to clarify which operation was performed
        df.columns = [f'{col}_{"Sum" if col in sum_fields else "Avg"}' for col in df.columns]

        if cumsum_operation:
            df = df.sort_values(list_of_grp_by_fields[0])
            df['cumulative_sum'] = df['Clicks_Sum'].cumsum()

        if ranking_operation:
            df['revenue_rank'] = df['Revenue_Sum'].rank(method='dense', ascending=False)

        # Reset index to make 'Device' and 'Market' regular columns again
        df = df.reset_index()

    return df


@st.cache_data()
def aggregating_pandas_cached(df: pd.DataFrame,
                              list_of_grp_by_fields=None,
                              cumsum_operation=None,
                              ranking_operation=None,
                              ) -> pd.DataFrame:
    return aggregating_pandas(df, list_of_grp_by_fields, cumsum_operation, ranking_operation)


def aggregating_polars(df: pl.DataFrame,
                       list_of_grp_by_fields=None,
                       cumsum_operation=None,
                       ranking_operation=None,
                       ) -> pl.DataFrame:
    if list_of_grp_by_fields:
        if 'Date' in list_of_grp_by_fields:
            df = df.with_columns(pl.col('Date').cast(pl.Date))

        agg_exprs = [
            *[pl.col(field).sum().alias(f"{field}_Sum") for field in sum_fields],
            *[pl.col(field).mean().alias(f"{field}_Avg") for field in mean_fields]
        ]

        df = df.group_by(list_of_grp_by_fields).agg(agg_exprs)

        if cumsum_operation:
            df = df.sort(list_of_grp_by_fields[0])
            df = df.with_columns(pl.col("Clicks_Sum").cum_sum().alias("cumulative_sum"))

        if ranking_operation:
            df = df.with_columns(pl.col('Revenue_Sum').rank('dense', descending=True).alias('revenue_rank'))

    return df

def _clean_tag(tag):
    # Remove underscores
    tag = tag.replace('_', ' ')

    # Convert to title case
    tag = tag.title()

    # Handle numbers separately to keep them as they are
    tag = re.sub(r'(\d+)', lambda x: x.group(1), tag)

    return tag


def aggregation_execution_time(loaded_data, dataframes_dict, df_tag, tag, list_of_grp_by_fields,
                               cumsum_operation, ranking_operation, data_format='pandas_filtering',):
    clean_tag = _clean_tag(tag)

    st.write(clean_tag)
    start_time = time.time()

    if data_format == 'pandas':
        aux_df = aggregating_pandas(df=loaded_data[df_tag]['dataframe'], list_of_grp_by_fields=list_of_grp_by_fields,
                                    cumsum_operation=cumsum_operation, ranking_operation=ranking_operation)
    elif data_format == 'pandas_cached':
        aux_df = aggregating_pandas_cached(df=loaded_data[df_tag]['dataframe'], list_of_grp_by_fields=list_of_grp_by_fields,
                                           cumsum_operation=cumsum_operation, ranking_operation=ranking_operation)
    elif data_format == 'polars':
        aux_df = aggregating_polars(df=loaded_data[df_tag]['dataframe'], list_of_grp_by_fields=list_of_grp_by_fields,
                                    cumsum_operation=cumsum_operation, ranking_operation=ranking_operation
                                    )
    else:
        aux_df = aggregating_pandas(df=loaded_data[df_tag]['dataframe'])

    execution_time = time.time() - start_time

    dataframes_dict[tag] = {
        'dataframe': aux_df,
        'execution_time': execution_time
    }

    return dataframes_dict
