# fMRI Preprocess

This folder includes [fmriprep](https://fmriprep.org/en/stable/) scripts which you can run either through docker or singularity(HPC). The singularity script is designed for [Sherlock](https://www.sherlock.stanford.edu/docs/getting-started/)

## FSL License
The scripts are required to use FSL license, and you can obtain the license from [here](https://surfer.nmr.mgh.harvard.edu/registration.html).
Set the license to right path for the scripts.

## Docker

Please refer to the installation [documents](https://fmriprep.org/en/stable/installation.html). 
You can install in-short by using:

    python -m pip install fmriprep-docker
Set inputs BIDS dataset path and FS_LICENSE:

    bids_root_dir=$HOME/TO/Dataset
    export  FS_LICENSE=$HOME/Documents/fsl_license.txt
 Run script:
 

    source fmriprep_docker.sh

## Singularity

[Singularity](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html) is a container platform designed for HPC. Please make sure that your HPC installed Singularity first. You may use: `module load` to load related modules.

To install the fmriprep singularity container, please download fmriprep.tar from [here](https://docs.sylabs.io/guides/3.5/user-guide/introduction.html).
After downloading the file, convert the tarball to Singularity Image:

    singularity build --sandbox fmriprep.simg docker-archive://fmriprep.tar

The scripts are built based on Sherlock, Stanford University. 
Change the Path FSL License at `fmriprep_singularity.sh`:
 `export  FS_LICENSE=$HOME/fsl_license.txt`
Change the `bids_root_dir` at `fmriprep_preproc.py`:
 `bids_root_dir  =  'PATH_TO_YOUR_BIDS_DATASET'`
 Run the python script for all subjects in the BIDS dataset:
 

    python fmriprep_preproc.py

