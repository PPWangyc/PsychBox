import os
import json

# list directories under the data directory
data_dir = '/oak/stanford/groups/fvlin/ACT/data/bids/T1_baseline/ASU'
dirs = os.listdir(data_dir)

# only remain directories that contain 'sub-'
dirs = [d for d in dirs if 'sub-' in d]
for subj in dirs:
    subj_path = os.path.join(data_dir, subj)
    # find all ses- directories
    ses_dirs = os.listdir(subj_path)
    ses_dir_path = os.path.join(subj_path, 'ses-01')
    func_dir = os.path.join(ses_dir_path, 'func')
    # find json files in the func directory
    func_files = os.listdir(func_dir)
    json_files = [f for f in func_files if f.endswith('.json')]
    assert len(json_files) == 1, f'Found {len(json_files)} json files in {func_dir}'

    # load the json file
    json_file = json_files[0]
    json_path = os.path.join(func_dir, json_file)
    with open(json_path, 'r') as f:
        data = json.load(f)
    # get the slice timing
    slice_timing = data['SliceTiming']

    # slice timing/10
    slice_timing = [round(t/10, 3) for t in slice_timing]
    # remove the json file
    os.remove(json_path)
    # update the json file
    data['SliceTiming'] = slice_timing
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Updated {json_path}')
print('Done')