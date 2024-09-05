import os
import glob
import argparse

argparser = argparse.ArgumentParser(description='Run 1st level analysis using FSL FEAT')

argparser.add_argument('--bids_root_dir', type=str, required=True,
                        help='Path to the BIDS root directory')
argparser.add_argument('--template_fsf', type=str, default='temp_1st_level_analysis.fsf',
                        help='Path to the template fsf file')

args = argparser.parse_args()

# get processed fmriprep subjects
fmriprep_dir= os.path.join(args.bids_root_dir, 'derivatives','fmriprep')
fmriprep_subs = [f for f in os.listdir(fmriprep_dir) if os.path.isdir(os.path.join(fmriprep_dir, f))]
fmriprep_subs = [f for f in fmriprep_subs if f.startswith('sub-')]

timestamp_dir = os.path.join(args.bids_root_dir, 'derivatives', 'timestamps')

with open(args.template_fsf, 'r') as f:
    fsf_file = f.readlines()

FSLDIR = os.environ['FSLDIR']

identifier = "/Users/PPWang"
fail_list = []
for sub in fmriprep_subs:
    try:
        # get the nii.gz files
        nii_files = glob.glob(os.path.join(fmriprep_dir, sub, 'func', 'sub-*space-MNI152NLin2009*_desc-preproc_bold*.nii.gz'))
        assert len(nii_files) == 1, f"More than one nii.gz file found for {sub}"
        nii_file = nii_files[0]
        # get the timestamp files
        timestamp_files = glob.glob(os.path.join(timestamp_dir, sub, '*.txt'))
        # sort the timestamp files
        timestamp_files.sort()
        
        output_dir = os.path.join(args.bids_root_dir, 'derivatives', 'feat', sub, '1st_level')
        os.makedirs(output_dir,  exist_ok=True)

        for i, line in enumerate(fsf_file):
            # set the output directory in the fsf file

            if 'set fmri(outputdir)' in line:
                fsf_file[i] = f'set fmri(outputdir) "{output_dir}"\n'
            # set the nii file in the fsf file
            if 'set fmri(regstandard) ' in line:
                fsf_file[i] = f'set fmri(regstandard) "{FSLDIR}/data/standard/MNI152_T1_2mm_brain"\n'
            # set the nii file in the fsf file
            if 'set feat_files(1)' in line:
                fsf_file[i] = f'set feat_files(1) "{nii_file}"\n'

        # set timestamp files
        for i, line in enumerate(fsf_file):
            if 'set fmri(custom' in line:
                ev_num = int(line.split('custom')[1].split(')')[0])
                fsf_file[i] = f'set fmri(custom{ev_num}) "{timestamp_files[ev_num- 1]}"\n'

        # write the fsf file
        output_fsf = os.path.join(output_dir, f'{sub}_1st_level_analysis.fsf')
        with open(output_fsf, 'w') as f:
            f.writelines(fsf_file)

        # run feat
        os.system(f'feat {output_fsf}')
    except Exception as e:
        fail_list.append(sub)
        print(f"Failed for {sub}, {e}")

if fail_list:
    print(f"Failed for {fail_list}")
else:
    print(f"Success for all subjects")