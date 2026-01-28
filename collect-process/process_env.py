from pathlib import Path
import pandas as pd
from functools import reduce

base_path = Path("./data/tidesandcurrents/")

dfs = []

for f in sorted(base_path.glob("met*.csv")):
    df = pd.read_csv(f)

    df.drop(columns=['Humidity (%)', 'Visibility (km)', 'Time (GMT)'], inplace=True)

    df["Date"] = pd.to_datetime(df["Date"])
    df["date"] = df["Date"].dt.strftime("%Y%m%d")
    df = df.drop(columns=["Date"])

    # Force numeric columns
    for col in df.columns:
        if col != "date":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.rename(columns={
        "Wind Speed (m/s)": "wind_speed_ms",
        "Wind Dir (deg)": "wind_dir_deg",
        "Wind Gust (m/s)": "wind_gust_ms",
        "Air Temp (°C)": "air_temp_c",
        "Baro (mb)": "baro_mb",
    })

    dfs.append(df)

# Combine all months and average by date
all_data = pd.concat(dfs, ignore_index=True)
meteor = all_data.groupby('date', as_index=False).mean()

# meteor.to_csv(out_path, index=False)

files = ["waterlevel-day-23-24.csv", "waterlevel-day-24-25.csv", "waterlevel-day-25-26.csv" ]

dfs.clear()

for fname in files:
    df = pd.read_csv(base_path / fname, na_values='-')
    df.drop(columns=['Time (GMT)', 'Preliminary (m)'], inplace=True)
    
    df["Date"] = pd.to_datetime(df["Date"])
    df["date"] = df["Date"].dt.strftime("%Y%m%d")
    df = df.drop(columns=["Date"])

    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.rename(columns={
        "Predicted (m)": "waterlevel_predicted_m",
        "Verified (m)": "waterlevel_verified_m",
    })

    dfs.append(df)

all_data = pd.concat(dfs, ignore_index=True)
water_level = all_data.groupby('date', as_index=False).mean()
# water_level.to_csv(out_path, index=False)

###
### second part
###

base_path = Path("./data/")
files = sorted(base_path.glob("*.csv"))

dfs = []

for f in files:
    var_name = f.stem.lower()

    # skip metadata row
    df = pd.read_csv(f, skiprows=[1])

    df["time"] = pd.to_datetime(df["time"], utc=True)
    df = df[(df["time"] >= "2023-01-01") & (df["time"] < "2026-01-01") ]

    value_col = [c for c in df.columns if c != "time" and not c.endswith("_qc_agg")][0]
    df = df[["time", value_col]]

    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    df["date"] = df["time"].dt.strftime("%Y%m%d")
    df.drop(columns=["time"], inplace=True)

    daily = (df.groupby("date", as_index=False).mean().round(3))

    dfs.append(daily)

env_df = reduce(lambda left, right: pd.merge(left, right, on="date", how="outer"), dfs)

# Merge meteorological and water level data (from first part)
env_df = pd.merge(env_df, meteor, on="date", how="left")
env_df = pd.merge(env_df, water_level, on="date", how="left")

env_df = env_df.sort_values("date").reset_index(drop=True)
env_df.to_csv("./processed/environment_all.csv", index=False)