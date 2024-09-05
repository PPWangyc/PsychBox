import pandas as pd

STIM_DICT = {'housework': 0, 'writing': 1, 'party': 2, 'shopping': 3, 'exercising': 4, 'dancing': 5, 'restaurant': 6, 'internet': 7, 'cooking': 8, 'funeral': 9, 'barbecue': 10, 'resting': 11, 'reading': 12, 'bathing': 13, 'wedding': 14, 'museum': 15, 'telephoning': 16, 'festival': 17, 'driving': 18, 'movie': 19}
CLUSTER_DICT = {
    1: ['housework', 'exercising', 'driving', 'shopping', 'dancing'],
    2: ['resting', 'reading', 'writing', 'bathing', 'internet'],
    3: ['cooking', 'movie', 'restaurant', 'barbecue', 'party', 'wedding', 'festival'],
    4: ['telephoning', 'museum', 'funeral']
}

# Function to parse the text file and extract the data into a DataFrame
def parse_stim_timestamps(file_path):
    # Initialize an empty DataFrame to store all runs data
    all_runs_df = pd.DataFrame(columns=["Stimulus", "Display_on_sec", "Display_off_sec"])
    
    # Read the entire file and split into lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Temporary list to hold data of a single run
    current_run_data = []
    
    for line in lines:
        if "Run_number" in line:
            # If starting a new run and there's existing data from previous run, append it to DataFrame
            if current_run_data:
                run_df = pd.DataFrame(current_run_data, columns=["Stimulus", "Display_on_sec", "Display_off_sec"])
                all_runs_df = pd.concat([all_runs_df, run_df], ignore_index=True)
                current_run_data = []
        else:
            # Split the line into components and strip to remove leading/trailing whitespaces
            parts = line.strip().split('\t')
            if len(parts) == 3:  # To ensure it's a valid data line
                current_run_data.append(parts)
    
    # Append the last run data to the DataFrame
    if current_run_data:
        run_df = pd.DataFrame(current_run_data, columns=["Stimulus", "Display_on_sec", "Display_off_sec"])
        all_runs_df = pd.concat([all_runs_df, run_df], ignore_index=True)
    
    # remove rows is "Stimulus Display_on_sec Display_off_sec" is present
    all_runs_df = all_runs_df[all_runs_df["Stimulus"] != "Stimulus"]
    # ignore index
    all_runs_df.reset_index(drop=True, inplace=True)
    # remove "A" or "An" and "scenario" from stimuli
    # all_runs_df["Stimulus"] = all_runs_df["Stimulus"].str.replace("A", "").str.replace("scenario", "").str.strip().str.lower()
    all_runs_df["Stimulus"] = all_runs_df["Stimulus"].str.replace("A", "").str.replace("n ", "").str.replace("scenario", "").str.strip().str.lower()

    # assert 100 rows
    assert all_runs_df.shape[0] == 100, f"Expected 100 rows, got {all_runs_df.shape[0], file_path}"

    # Map the stimuli to their respective indices
    all_runs_df["stim_idx"] = all_runs_df["Stimulus"].map(STIM_DICT)

    # remain 2 decimal places for onset and offset
    all_runs_df["Display_on_sec"] = all_runs_df["Display_on_sec"].astype(float).round(1)
    all_runs_df["Display_off_sec"] = all_runs_df["Display_off_sec"].astype(float).round(1)

    # change column names
    all_runs_df.columns = ["scenario", "onset", "offset", "stim_idx"]
    # add another column called duration
    all_runs_df["duration"] = all_runs_df["offset"].astype(float) - all_runs_df["onset"].astype(float)

    # add a column called cluster
    all_runs_df["cluster"] = 0
    for cluster, stimuli in CLUSTER_DICT.items():
        all_runs_df.loc[all_runs_df["scenario"].isin(stimuli), "cluster"] = cluster

    # assert no NaN values
    assert all_runs_df.isnull().sum().sum() == 0, f"NaN values found in {file_path}, {all_runs_df}"

    return all_runs_df

def get_scenario_timestamp(df):
    scenario_timestamp_dict = {}
    for stim in STIM_DICT.keys():
        stim_df = df[df["scenario"] == stim]
        assert stim_df.shape[0] == 5, f"Expected 5 rows for {stim}, got {stim_df.shape[0]}"
        # add a new column called parametric_modulation
        stim_df["parametric_modulation"] = 1

        # stim_df drop offset, stim_idx, cluster columns
        stim_df = stim_df.drop(["scenario","offset", "stim_idx", "cluster"], axis=1)
        # ignore index
        stim_df.reset_index(drop=True, inplace=True)
        scenario_timestamp_dict[stim] = stim_df
    return scenario_timestamp_dict