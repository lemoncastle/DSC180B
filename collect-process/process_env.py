from pathlib import Path
import pandas as pd
from functools import reduce

base_path = Path("./data/tidesandcurrents/")

dfs = []

for i in range(1, 13):
    df = pd.read_csv(base_path / f"meteor{i}.csv")
    df.drop(columns=['Humidity (%)', 'Visibility (km)', 'Time (GMT)'], inplace=True)
    
    df["Date"] = pd.to_datetime(df["Date"])
    df["date"] = df["Date"].dt.strftime("%Y%m%d")
    df = df.drop(columns=["Date"])

    # Force numeric columns
    for col in df.columns:
        if col != 'date':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
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

files = ["waterlevel-day-24-25.csv", "waterlevel-day-25-26.csv" ]

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
files = sorted(base_path.glob("*.csv"))  # your 16 CSVs

dfs = []

for f in files:
    # get filename without extension as variable name
    var_name = f.stem  
    df = pd.read_csv(f)
    
    # Use Start date, convert to string YYYYMMDD
    df["date"] = df["Start date"].str[:10].str.replace("-", "")
    
    # Rename metrics to include variable
    df = df.rename(columns={
        "Mean": f"{var_name}_mean",
        "Min": f"{var_name}_min",
        "Max": f"{var_name}_max"
    })

    # Keep only date + renamed metrics
    df = df[["date", f"{var_name}_mean", f"{var_name}_min", f"{var_name}_max"]]
    dfs.append(df)

env_df = reduce(lambda left, right: pd.merge(left, right, on="date", how="outer"), dfs)

# Merge meteorological and water level data (from first part)
env_df = pd.merge(env_df, meteor, on="date", how="left")
env_df = pd.merge(env_df, water_level, on="date", how="left")

env_df = env_df.sort_values("date").reset_index(drop=True)
env_df.to_csv("./processed/environment_all.csv", index=False)