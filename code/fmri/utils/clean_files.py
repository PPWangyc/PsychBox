# 
import os

# list directories under the data directory
data_dir = '/oak/stanford/groups/fvlin/ACT/data/bids/T1_baseline/UR'
dirs = os.listdir(data_dir)
# only remain directories that contain 'sub-'
dirs = [d for d in dirs if 'sub-' in d]
for subj in dirs:
    subj_path = os.path.join(data_dir, subj)
    # find all ses- directories
    ses_dirs = os.listdir(subj_path)
    ses_dirs = [d for d in ses_dirs if 'ses-' in d]
    if len(ses_dirs) == 0:
        print(f'No ses- directory found for {subj}')
        raise ValueError('No ses- directory found')
    elif len(ses_dirs) == 1:
        print(f'Found ses- directory for {subj}')
        # change the name of the ses- directory to ses-01
        ses_dir = ses_dirs[0]
        ses_dir_path = os.path.join(subj_path, ses_dir)
        ses_dir_new = os.path.join(subj_path, 'ses-01')
        os.rename(ses_dir_path, ses_dir_new)
        print(f'Renamed {ses_dir} to ses-01')
    else:
        print(f'Multiple ses- directories found for {subj}')
        print(ses_dirs)
        print('')
        raise ValueError('Multiple ses- directories found')
    ses_dir_path = os.path.join(subj_path, 'ses-01')
    # remove .mif files 
    files = os.listdir(ses_dir_path)
    files = [f for f in files if '.mif' in f]
    for f in files:
        f_path = os.path.join(ses_dir_path, f)
        os.remove(f_path)
        print(f'Removed {f}')
    # remove folder start with dwifslpreproc
    files = os.listdir(ses_dir_path)
    files = [f for f in files if 'dwifslpreproc' in f]
    for f in files:
        folder_path = os.path.join(ses_dir_path, f)
        os.system(f'rm -rf {folder_path}')
        print(f'Removed {f}')
    print('')

    func_path = os.path.join(ses_dir_path, 'func')
    # check how many files end with .nii.gz
    files = os.listdir(func_path)
    files = [f for f in files if f.endswith('.nii.gz')]
    if len(files) == 0:
        print(f'No .nii.gz files found for {subj}')
        raise ValueError('No .nii.gz files found')
    elif len(files) == 1:
        print(f'Found .nii.gz file for {subj}')
    else:
        print(f'Multiple .nii.gz files found for {subj}')
        print(files)
        print('')
        raise ValueError('Multiple .nii.gz files found')
    
    # remove file name is bvals, bvecs, and dwi.nii.gz in ses_dir_path/dwi
    dwi_path = os.path.join(ses_dir_path, 'dwi')
    for root, dirs, files in os.walk(dwi_path):
        for f in files:
            if f in ['bvals', 'bvecs', 'dwi.nii.gz']:
                f_path = os.path.join(root, f)
                os.remove(f_path)
                print(f'Removed {f}')

    # rename the file name in ses_dir_path anat
    anat_path = os.path.join(ses_dir_path, 'anat')
    for root, dirs, files in os.walk(anat_path):
        for f in files:
            if "T1w_defaced.nii.gz" in f:
                f_path = os.path.join(root, f)
                f_new = os.path.join(root, f.replace('_defaced', ''))
                os.rename(f_path, f_new)
                print(f'Renamed {f} to {f_new}')
            if "FLAIR_defaced.nii.gz" in f:
                f_path = os.path.join(root, f)
                f_new = os.path.join(root, f.replace('_defaced', ''))
                os.rename(f_path, f_new)
                print(f'Renamed {f} to {f_new}')
    

                


