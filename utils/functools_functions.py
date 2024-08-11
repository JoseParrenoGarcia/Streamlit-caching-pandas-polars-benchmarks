import os
import pandas as pd
import time
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
    return pd.concat(df_list, ignore_index=True)


@functools.lru_cache
def filtering_functools(folder_path, dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None):
    df = read_and_combine_csv_files_pandas_cached_functools(folder_path)

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


    return df

@functools.lru_cache
def filtering_and__aggregating_functools(folder_path,
                                         dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
                                         list_of_grp_by_fields=None
                                         ):
    df = read_and_combine_csv_files_pandas_cached_functools(folder_path)

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


def functools_etl(folder_path,
                  dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
                  list_of_grp_by_fields=None
                  ):
    print('')
    print('----------------------------------------------------------------------------------------')
    print(folder_path)
    print('----------------------------------------------------------------------------------------')
    start_time = time.time()
    df_read = read_and_combine_csv_files_pandas_cached_functools(folder_path)
    execution_time = time.time() - start_time
    print('Read execution time in seconds: {}'.format(execution_time))

    start_time = time.time()
    # Convert mutable arguments to immutable types
    immutable_device_filter = tuple(device_filter) if device_filter else None
    immutable_market_filter = tuple(market_filter) if market_filter else None
    immutable_ROI_filter = tuple(ROI_filter) if ROI_filter else None

    df_filter = filtering_functools(folder_path=folder_path,
                                    dates_filter=dates_filter,
                                    device_filter=immutable_device_filter,
                                    market_filter=immutable_market_filter,
                                    ROI_filter=immutable_ROI_filter)
    execution_time = time.time() - start_time
    print('Filter execution time in seconds: {}'.format(execution_time))

    start_time = time.time()
    # Convert mutable arguments to immutable types
    immutable_list_of_grp_by_fields = tuple(list_of_grp_by_fields) if list_of_grp_by_fields else None
    df_filter_and_agg = filtering_and__aggregating_functools(folder_path=folder_path,
                                                             dates_filter=dates_filter,
                                                             device_filter=immutable_device_filter,
                                                             market_filter=immutable_market_filter,
                                                             ROI_filter=immutable_ROI_filter,
                                                             list_of_grp_by_fields=immutable_list_of_grp_by_fields,
                                                             )
    execution_time = time.time() - start_time
    print('Filter & aggregation execution time in seconds: {}'.format(execution_time))

    return df_filter_and_agg
