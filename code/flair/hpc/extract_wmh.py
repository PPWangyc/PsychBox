import os
import glob
import argparse
import pandas as pd
from bs4 import BeautifulSoup
import re
# load module:
# ml py-pandas/1.0.3_py36

# set up the argument parser
parser = argparse.ArgumentParser(description='Run fmriprep on all subjects in a BIDS dataset')
parser.add_argument('--bids_root_dir', type=str, help='The root directory of the BIDS dataset')
args = parser.parse_args()

bids_root_dir = args.bids_root_dir
# get subject list under bids_root_dir
subject_list = [x.split('/')[-1] for x in glob.glob(os.path.join(bids_root_dir, 'sub-*'))]
subject_list = [x.split('-')[-1] for x in subject_list]
print(subject_list)
# check if bids_root_dir has derivatives folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives'))
# check if bids_root_dir/derivatives has fmriprep folder
if not os.path.exists(os.path.join(bids_root_dir, 'derivatives', 'spm')):
    os.mkdir(os.path.join(bids_root_dir, 'derivatives', 'spm'))

df = pd.DataFrame(columns=['subject', 'session', 'lesion_volume'])
for subject in subject_list:
    html_path = os.path.join(bids_root_dir, 'derivatives','spm', 'sub-{}'.format(subject), 'ses-*', 'anat', 'report_LST_lpa_mwsub-{}*FLAIR_preproc.html'.format(subject))
    html_files = glob.glob(html_path)
    print(html_path)
    assert len(html_files) == 1, 'Incorrect number of HTML files found for subject {}: {}'.format(subject, html_files)
    html_file = html_files[0]
    session = html_file.split('/')[-3]
    # read html file
    with open(html_file, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    # Find the table data containing "Lesion volume"
    volume_text = soup.find(text=re.compile('Lesion volume'))
    if volume_text:
        volume_td = volume_text.find_next('td')  # Find the next td element after the "Lesion volume" text
        lesion_volume = volume_td.text.strip() if volume_td else 'Volume not found'
    else:
        lesion_volume = 'Volume not found'

    # Print or process the lesion volume
    print("Lesion Volume:", lesion_volume)
    # create a dataframe to store the lesion volume
    df = df.append({'subject': subject, 'session': session, 'lesion_volume': lesion_volume}, ignore_index=True)
    # save the dataframe to a csv file
csv_file = os.path.join(bids_root_dir, 'derivatives', 'spm', 'lesion_volume.csv')
df.to_csv(csv_file, index=False)

print('Done!')
