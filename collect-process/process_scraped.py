from datetime import datetime
from pathlib import Path
import pandas as pd
import glob
import os
s = datetime.now()

base_path = "./ifcb_downloads1/"
burger = Path(base_path) # used for iterating months I'm kinda hungry
out_dir = Path("./processed/")
out_dir.mkdir(parents=True, exist_ok=True)

def read_hdr(path: Path) -> dict:
    return { k.strip(): v.strip()
            for line in path.read_text().splitlines()
            if ":" in line
            for k, v in [line.split(":", 1)] }

samples = []
ml_samples = []

# iterate through each month directory
for month_dir in sorted(burger.iterdir()):
    path = base_path + month_dir.name + "/"
    print(f"Processing files in {path}... {(datetime.now()- s).total_seconds()}s")
    
    # read ml analyzed file for month, group by date and append
    ml_file = Path(path) / f"ml_{month_dir.name[-2:]}.csv"
    ml_df = pd.read_csv(ml_file).groupby('date', as_index=True).mean()
    ml_samples.append(ml_df)

    # for each hdr file in month folder get date and find matching files (with date)
    for files in glob.glob(path + '*.hdr'):
        timestamp = os.path.basename(files).split('_')[0].lstrip('D')
        date = timestamp.split('T')[0]
        
        # read files with matching timestamp (1 bin)
        for match in glob.glob(os.path.join(path, f"*{timestamp}*")):
            if match.endswith('.csv'):
                if "_features" in match:
                    try:
                        features = pd.read_csv(Path(match))
                        features.drop(columns=['roi_number'], inplace=True)
                    except pd.errors.EmptyDataError:
                        features = None
                        print(f"Features file is empty for date {timestamp}")
                else:
                    try:
                        class_scores = pd.read_csv(Path(match), usecols=['pid', 'Lingulodinium_polyedra'])
                    except pd.errors.EmptyDataError:
                        class_scores = None
                        print(f"Class scores file is empty for date {timestamp}")
            elif match.endswith('hdr'):
                hdr = read_hdr(Path(match))
                roi_count = float(hdr["roiCount"])
        
        # if both files read, calculate expected values and append
        if isinstance(features, pd.DataFrame) and isinstance(class_scores, pd.DataFrame):
            weights = class_scores["Lingulodinium_polyedra"]
            weighted_means = (features.multiply(weights, axis=0).sum()/ weights.sum())
            sample_row = {
                "date": date,
                "roiCount": roi_count,
                "Lpoly_expected": weights.sum(),
                }
            for col, val in weighted_means.items():
                sample_row[col] = val
            samples.append(sample_row)

# make dataframes, merge and calculate Lpoly per ml
samples_df = pd.DataFrame(samples)
samples_df["date"] = samples_df["date"].astype("int64")
ml_df_all = pd.concat(ml_samples).reset_index()

daily = samples_df.groupby("date", as_index=False).mean().merge(ml_df_all, on="date", how="left")

daily["Lpoly_expected_ml"] = daily["Lpoly_expected"] / daily["ml_analyzed"]
daily["ROI_per_ml"] = daily["roiCount"] / daily["ml_analyzed"]

# reorder columns to have important ones first
important = ["date", "roiCount", "ml_analyzed", "ROI_per_ml", "Lpoly_expected", "Lpoly_expected_ml"]
all_cols = daily.columns.tolist()
other_cols = [c for c in all_cols if c not in important]
new_order = important + other_cols
daily = daily[new_order]
daily.head()

out_file = out_dir / "processed.csv"
daily.to_csv(out_file, index=False)
print(f"Processing complete in {(datetime.now()- s).total_seconds()}s yay")