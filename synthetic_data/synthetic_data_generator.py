import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_dataset(num_rows,
                     start_date=datetime(2023, 1, 1),
                     end_date=datetime(2024, 12, 31),
                     max_rows_per_file=200_000,
                     ):

    # Generate random dates
    date_range = pd.date_range(start=start_date, end=end_date, periods=num_rows).date

    # Generate other columns
    impressions = np.random.randint(0, 10_000_001, num_rows)
    ctr = np.round(np.random.random(num_rows), 3)
    clicks = (impressions * ctr).astype(int)
    cpc = np.round(np.random.uniform(0.10, 2.35, num_rows), 3)
    cost = np.round(clicks * cpc, 3)
    roi = np.round(np.random.uniform(0.75, 1.55, num_rows), 3)
    revenue = np.round(cost * roi, 3)
    device = np.random.choice(['Desktop', 'Mobile'], num_rows)

    # Create DataFrame
    df = pd.DataFrame({
        'Date': date_range,
        'Impressions': impressions,
        'CTR': ctr,
        'Clicks': clicks,
        'CPC': cpc,
        'Cost': cost,
        'ROI': roi,
        'Revenue': revenue,
        'Device': device
    })

    # Save as CSV and Parquet
    # -> Because Github doesnt allow files larger than 100mb, I had to split bigger files into smaller parts.

    # Determine the number of files needed
    num_files = (num_rows // max_rows_per_file) + (1 if num_rows % max_rows_per_file > 0 else 0)

    for i in range(num_files):
        start_idx = i * max_rows_per_file
        end_idx = min((i + 1) * max_rows_per_file, num_rows)
        subset_df = df.iloc[start_idx:end_idx]

        # CSV
        output_dir_csv = f'data_csv/dataset_{num_rows}'
        os.makedirs(output_dir_csv, exist_ok=True)
        csv_filename = os.path.join(output_dir_csv, f'dataset_{num_rows}_subset{i + 1}.csv')
        subset_df.to_csv(csv_filename, index=False)

        # Parquet
        output_dir_parquet = f'data_parquet/dataset_{num_rows}'
        os.makedirs(output_dir_parquet, exist_ok=True)
        parquet_filename = os.path.join(output_dir_parquet, f'dataset_{num_rows}_subset{i + 1}.parquet')
        subset_df.to_parquet(parquet_filename, index=False)

    return df

# Generate datasets
datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]

for num_rows in datasets:
    generate_dataset(num_rows)