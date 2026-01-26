from datetime import datetime
from pathlib import Path
import pandas as pd

base_path = Path("./data/tidesandcurrents/")
out_path = Path("./processed/processed_meteor.csv")

dfs = []

for i in range(1, 13):
    df = pd.read_csv(base_path / f"meteor{i}.csv")

    df.drop(columns=['Humidity (%)', 'Visibility (km)', 'Time (GMT)'], inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])

    # Force numeric columns
    for col in df.columns:
        if col != 'Date':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    dfs.append(df)

# Combine all months and average by date
all_data = pd.concat(dfs, ignore_index=True)
check = all_data.groupby('Date', as_index=False).mean().round(3)

check.to_csv(out_path, index=False)

files = ["waterlevel-day-24-25.csv", "waterlevel-day-25-26.csv" ]

dfs.clear()
out_path = Path("./processed/processed_waterlevel.csv")

for fname in files:
    df = pd.read_csv(base_path / fname, na_values='-')

    df['Date'] = pd.to_datetime(df['Date'])
    df.drop(columns=['Time (GMT)', 'Preliminary (m)'], inplace=True)

    for col in df.columns:
        if col != 'Date':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    dfs.append(df)

all_data = pd.concat(dfs, ignore_index=True)
check = all_data.groupby('Date', as_index=False).mean().round(3)
check.to_csv(out_path, index=False)