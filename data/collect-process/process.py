from datetime import datetime
from pathlib import Path
import pandas as pd
import glob
import os
s = datetime.now()

base_path = "./ifcb_downloads/"
burger = Path(base_path) # used for iterating months I'm kinda hungry
out_dir = Path("./processed/")
out_dir.mkdir(parents=True, exist_ok=True)

# iterate through each month directory
for month_dir in sorted(burger.iterdir()):
    path = base_path + month_dir.name + "/"
    print(f"Processing files in {path}... {(datetime.now()- s).total_seconds()}s")
    
    # for each hdr file in month folder get date and find matching files (with date)
    for files in glob.glob(path + '*.hdr'):
        date = os.path.basename(files).split('_')[0].lstrip('D')
        # read in files per date as dfs and combine
        for match in glob.glob(os.path.join(path, f"*{date}*")):
            if match.endswith('.csv'):
                if "_features" in match:
                    try:
                        features = pd.read_csv(Path(match))
                        features.drop(columns=['roi_number'], inplace=True)
                    except pd.errors.EmptyDataError:
                        features = pd.DataFrame()
                        print(f"Features file is empty for date {date}")
                else:
                    try:
                        class_scores = pd.read_csv(Path(match), usecols=['pid', 'Lingulodinium_polyedra'])
                    except pd.errors.EmptyDataError:
                        class_scores = pd.DataFrame()
                        print(f"Class scores file is empty for date {date}")
            else:
                # hdr = read_hdr(Path(match))
                # the tempperatures are probably the temperature of the machine not the water
                # since temperatures fluctuate 27 so probably celsius so it's been ommited
                continue
                          
        # combine and save (shouldn't break if one of the dfs is empty)
        combined = pd.concat([class_scores, features], axis=1)
        out_file = out_dir / f"{date}.csv"
        combined.to_csv(out_file, index=False)

print(f"Processing complete in {(datetime.now()- s).total_seconds()}s yay")