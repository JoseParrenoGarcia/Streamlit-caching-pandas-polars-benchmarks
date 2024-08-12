import pandas as pd


def execution_times_df(dataframes_dict):
    # Extracting the execution times in a dataframe so that we can plot
    execution_time_df = []

    for tag, info in dataframes_dict.items():
        execution_time_df.append({'Tag': tag, 'Execution Time': info['execution_time']})

    execution_time_df = pd.DataFrame(execution_time_df)
    execution_time_df['Number of rows'] = execution_time_df['Tag'].str.extract(r'dataframe_(\d+)')[0].astype(int)
    execution_time_df['Data format'] = execution_time_df['Tag'].str.extract(r'(pandas_to_polars|pandas_to_polars_cached|polars_to_pandas'
                                                                            r'|pandas|pandas_streamlit_cached|polars|'
                                                                            r'|pandas_functools_cached|polars_functools_cached)$')[0]

    return execution_time_df


def calculate_percent_diff_execution_times(execution_time_df, selected_baseline):
    # Create a pivot table with execution times
    pivot = execution_time_df.pivot(index='Number of rows', columns='Data format', values='Execution Time')

    # Get all columns except 'Number of rows'
    data_format_columns = [col for col in pivot.columns if col != 'Number of rows']

    # Calculate ratio
    ratio = pivot.copy()
    for c in data_format_columns:
        ratio[f'{c}_ratio'] = ratio[selected_baseline].astype('float') / ratio[c].astype('float')

    # Keep only ratio columns
    ratio = ratio.drop(columns=[selected_baseline] + data_format_columns + [f'{selected_baseline}_ratio']).reset_index()

    # Melt the dataframe to long format
    result_df = pd.melt(ratio, id_vars=['Number of rows'],
                        var_name='Data format', value_name='Ratio')

    # Round the ratio to 2 decimal places for readability
    result_df['Ratio'] = result_df['Ratio'].round(2)
    result_df['Data format'] = result_df['Data format'].str.replace('_ratio', '', regex=False)

    return result_df

