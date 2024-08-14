import time
from utils.read_data_functions import read_and_combine_csv_files_pandas, read_and_combine_csv_files_pandas_cached, read_and_combine_csv_files_polars
from utils.filtering_functions import filtering_pandas, filtering_pandas_cached, filtering_polars
from utils.aggregation_functions import aggregating_pandas, aggregating_pandas_cached, aggregating_polars
from utils.join_functions import join_pandas, join_pandas_cached, join_polars
from utils.functools_functions import pandas_functools_etl, polars_functools_etl
import pandas as pd
import polars as pl


def pandas_etl(folder_path, secondary_df=None,
               dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
               list_of_grp_by_fields=None,
               ):

    df = read_and_combine_csv_files_pandas(folder_path)
    df = filtering_pandas(df=df, dates_filter=dates_filter, device_filter=device_filter, market_filter=market_filter, ROI_filter=ROI_filter)
    df = join_pandas(df, secondary_df)
    df = aggregating_pandas(df=df, list_of_grp_by_fields=list_of_grp_by_fields)

    return df


def pandas_etl_streamlit_cached(folder_path, secondary_df=None,
                                dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
                                list_of_grp_by_fields=None,
                                ):

    df = read_and_combine_csv_files_pandas_cached(folder_path)
    df = filtering_pandas_cached(df=df, dates_filter=dates_filter, device_filter=device_filter, market_filter=market_filter, ROI_filter=ROI_filter)
    df = join_pandas_cached(df, secondary_df)
    df = aggregating_pandas_cached(df=df, list_of_grp_by_fields=list_of_grp_by_fields)

    return df


def polars_etl(folder_path, secondary_df=None,
               dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
               list_of_grp_by_fields=None
               ):

    df = read_and_combine_csv_files_polars(folder_path)
    df = filtering_polars(df=df, dates_filter=dates_filter, device_filter=device_filter, market_filter=market_filter, ROI_filter=ROI_filter)
    df = join_polars(df, secondary_df)
    df = aggregating_polars(df=df, list_of_grp_by_fields=list_of_grp_by_fields)

    return df


def etl_comparisons(folder_path, num_rows, dataframes_dict,
                    dates_filter=None, device_filter=None, market_filter=None, ROI_filter=None,
                    list_of_grp_by_fields=None
                    ):

    markets_pandas_df = pd.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')
    markets_polars_df = pl.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')

    print('')
    print('----------------------------------------------------------------------------------------')
    print(folder_path)
    print('----------------------------------------------------------------------------------------')

    tag = f'dataframe_{num_rows}_csv_pandas'

    start_time = time.time()
    pandas_df = pandas_etl(folder_path=folder_path,
                           secondary_df=markets_pandas_df,
                           dates_filter=dates_filter,
                           device_filter=device_filter,
                           market_filter=market_filter,
                           ROI_filter=ROI_filter,
                           list_of_grp_by_fields=list_of_grp_by_fields,
                           )
    execution_time = time.time() - start_time
    print('Pandas ETL execution time in seconds: {}'.format(execution_time))
    print('')

    dataframes_dict[tag] = {
        'dataframe': pandas_df,
        'execution_time': execution_time
    }

    # ----------------------------------------------------------------------------------------------------------------
    tag = f'dataframe_{num_rows}_csv_pandas_streamlit_cached'

    start_time = time.time()
    pandas_st_cached_df = pandas_etl_streamlit_cached(folder_path=folder_path,
                                                      secondary_df=markets_pandas_df,
                                                      dates_filter=dates_filter,
                                                      device_filter=device_filter,
                                                      market_filter=market_filter,
                                                      ROI_filter=ROI_filter,
                                                      list_of_grp_by_fields=list_of_grp_by_fields,
                                                      )
    execution_time = time.time() - start_time
    print('Pandas Streamlit Cached ETL execution time in seconds: {}'.format(execution_time))
    print('')

    dataframes_dict[tag] = {
        'dataframe': pandas_st_cached_df,
        'execution_time': execution_time
    }

    # ----------------------------------------------------------------------------------------------------------------
    tag = f'dataframe_{num_rows}_csv_pandas_functools_cached'

    # Convert mutable arguments to immutable types
    immutable_device_filter = tuple(device_filter) if device_filter else None
    immutable_market_filter = tuple(market_filter) if market_filter else None
    immutable_ROI_filter = tuple(ROI_filter) if ROI_filter else None
    immutable_list_of_grp_by_fields = tuple(list_of_grp_by_fields) if list_of_grp_by_fields else None

    start_time = time.time()
    pandas_functools_cached_df = pandas_functools_etl(folder_path=folder_path,
                                                      dates_filter=dates_filter,
                                                      device_filter=immutable_device_filter,
                                                      market_filter=immutable_market_filter,
                                                      ROI_filter=immutable_ROI_filter,
                                                      list_of_grp_by_fields=immutable_list_of_grp_by_fields,
                                                      )
    execution_time = time.time() - start_time
    print('Pandas functools cached ETL execution time in seconds: {}'.format(execution_time))
    print('')

    dataframes_dict[tag] = {
        'dataframe': pandas_functools_cached_df,
        'execution_time': execution_time
    }

    # ----------------------------------------------------------------------------------------------------------------
    tag = f'dataframe_{num_rows}_csv_polars'

    start_time = time.time()
    polars_df = polars_etl(folder_path=folder_path,
                           secondary_df=markets_polars_df,
                           dates_filter=dates_filter,
                           device_filter=device_filter,
                           market_filter=market_filter,
                           ROI_filter=ROI_filter,
                           list_of_grp_by_fields=list_of_grp_by_fields,
                           )
    execution_time = time.time() - start_time
    print('Polars ETL execution time in seconds: {}'.format(execution_time))
    print('')

    dataframes_dict[tag] = {
        'dataframe': polars_df,
        'execution_time': execution_time
    }

    # ----------------------------------------------------------------------------------------------------------------
    tag = f'dataframe_{num_rows}_csv_polars_functools_cached'

    start_time = time.time()
    polars_functools_cached_df = polars_functools_etl(folder_path=folder_path,
                                                      dates_filter=dates_filter,
                                                      device_filter=immutable_device_filter,
                                                      market_filter=immutable_market_filter,
                                                      ROI_filter=immutable_ROI_filter,
                                                      list_of_grp_by_fields=immutable_list_of_grp_by_fields,
                                                      )
    execution_time = time.time() - start_time
    print('Polars functools cached ETL execution time in seconds: {}'.format(execution_time))
    print('')

    dataframes_dict[tag] = {
        'dataframe': polars_functools_cached_df,
        'execution_time': execution_time
    }

    return dataframes_dict



