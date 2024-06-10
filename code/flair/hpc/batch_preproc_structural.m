% List of open inputs
nrun = 1; % enter the number of runs here
jobfile = {'/scratch/users/ppwang/Project/PsychBox/code/flair/hpc/batch_preproc_structural_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(0, nrun);
for crun = 1:nrun
end
inputs={flair_path}; 
spm('defaults', 'FMRI');
%spm_jobman('run', jobs);
spm_jobman('run', jobs, inputs{:});
