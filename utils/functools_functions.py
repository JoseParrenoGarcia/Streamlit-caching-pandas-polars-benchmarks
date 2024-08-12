import os
import pandas as pd
import polars as pl
import functools

# Fields to sum
sum_fields = ['Impressions', 'Clicks', 'Cost', 'Revenue']

# Fields to average
mean_fields = ['CTR', 'CPC', 'ROI']

# @functools.lru_cache decorator requires that all the arguments passed to the cached function be hashable.
# A pandas.DataFrame is mutable and therefore unhashable. Therefore, we always need to reference the read from CSV, as this is considered non-mutable.

@functools.lru_cache
def read_and_combine_csv_files_pandas_cached_functools(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]

    df = pd.concat(df_list, ignore_index=True)
    markets_pandas_df = pd.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')

    return pd.merge(df, markets_pandas_df, on='Market', how='inner')


@functools.lru_cache
def read_and_combine_csv_files_polars_cached_functools(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pl.read_csv(os.path.join(folder_path, file)) for file in csv_files]

    df = pl.concat(df_list)
    markets_polars_df = pl.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')

    return df.join(markets_polars_df, on='Market', how='inner')


@functools.lru_cache
def pandas_functools_etl(folder_path,
                         dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
                         list_of_grp_by_fields=None):
    df = read_and_combine_csv_files_pandas_cached_functools(folder_path)
    markets_pandas_df = pd.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')

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

    df = pd.merge(df, markets_pandas_df, on='Market', how='inner')

    if list_of_grp_by_fields:
        df = (df
              .groupby(list(list_of_grp_by_fields))
              .agg({**{field: 'sum' for field in sum_fields},
                    **{field: 'mean' for field in mean_fields}}
                   )
              )

        # Rename columns to clarify which operation was performed
        df.columns = [f'{col}_{"Sum" if col in sum_fields else "Avg"}' for col in df.columns]

        df = df.reset_index()

    return df

@functools.lru_cache
def polars_functools_etl(folder_path,
                         dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
                         list_of_grp_by_fields=None
                         ):
    df = read_and_combine_csv_files_polars_cached_functools(folder_path)
    markets_polars_df = pl.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')

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

    df.join(markets_polars_df, on='Market', how='inner')

    if list_of_grp_by_fields:
        if 'Date' in list_of_grp_by_fields:
            df = df.with_columns(pl.col('Date').cast(pl.Date))

        agg_exprs = [
            *[pl.col(field).sum().alias(f"{field}_Sum") for field in sum_fields],
            *[pl.col(field).mean().alias(f"{field}_Avg") for field in mean_fields]
        ]

        df = df.group_by(list_of_grp_by_fields).agg(agg_exprs)

    return df
