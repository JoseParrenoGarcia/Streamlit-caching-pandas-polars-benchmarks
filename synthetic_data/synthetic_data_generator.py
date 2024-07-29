import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_dataset(num_rows,
                     start_date=datetime(2023, 1, 1),
                     end_date=datetime(2024, 12, 31),
                     output_dir='data'):

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

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
    csv_filename = os.path.join(output_dir, f'dataset_{num_rows}.csv')
    parquet_filename = os.path.join(output_dir, f'dataset_{num_rows}.parquet')

    df.to_csv(csv_filename, index=False)
    df.to_parquet(parquet_filename, index=False)

    return df

# Generate datasets
# datasets = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
#
# for num_rows in datasets:
#     generate_dataset(num_rows, start_date, end_date, output_dir)