import os
import pandas as pd
import numpy as np
import glob
from utils import (parse_stim_timestamps,
                   get_scenario_timestamp,
                    STIM_DICT,
                        CLUSTER_DICT)

timestamp_dir = '/Users/ppwang/Data/harp_timestamps/'
output_dir = os.path.join(timestamp_dir, 'derivatives', "timestamps")

os.makedirs(output_dir, exist_ok=True)

# get every subject folder
subject_folders = [f for f in os.listdir(timestamp_dir) if os.path.isdir(os.path.join(timestamp_dir, f))]
# subj folder should start with sub-
subject_folders = [f for f in subject_folders if f.startswith('sub-')]
for sub in subject_folders:
    os.makedirs(os.path.join(output_dir, sub), exist_ok=True)
    # get timestamp files
    timestamp_files = glob.glob(os.path.join(timestamp_dir, sub, '*.txt'))

    assert len(timestamp_files) == 1, f"More than one timestamp file found for {sub}"
    timestamp_path = timestamp_files[0]
    timestamp_df = parse_stim_timestamps(timestamp_path)
    scenario_timestamp = get_scenario_timestamp(timestamp_df)
    for scenario, df in scenario_timestamp.items():
        scenario_idx = STIM_DICT[scenario] + 1
        # find cluster in dict
        for cluster, stimuli in CLUSTER_DICT.items():
            if scenario in stimuli:
                cluster_idx = cluster
                break
        if cluster_idx < 10:
            cluster_idx = f"0{cluster_idx}"
        if scenario_idx < 10:
            scenario_idx = f"0{scenario_idx}"

        output_path = os.path.join(output_dir, sub, f"{sub}_idx-{scenario_idx}_cluster-{cluster_idx}_{scenario}_timestamps.txt")
        print(f"Writing to {output_path}")
        print(df)
        # save ignore column names
        df.to_csv(output_path, sep='\t', index=False, header=False)
    output_path = os.path.join(output_dir, sub, f"{sub}_timestamps.csv")
    print(f"Writing to {output_path}")
    
    timestamp_df.to_csv(output_path, index=False)
    print(timestamp_df)

    