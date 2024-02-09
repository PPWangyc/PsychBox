# ECG

This folder includes sample code for preprocessing ECG during a fMRI session, and calculate Heart Rate Variability(HRV) using [Heartpy](https://python-heart-rate-analysis-toolkit.readthedocs.io/en/latest/).

## Run
The code only support 1-channel ECG analysis.
In `run.py`, set the `ECG_PATH  =  'PATH_TO_YOUR_ECG_TXT_FILE'`

We use a lowpass filter for removing the artifacts in fMRI session.
Set slices and TR, here is an example:

    slices  =  72

	TR  =  1.73

To run:

    python run.py