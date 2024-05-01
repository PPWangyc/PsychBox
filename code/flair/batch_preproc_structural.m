% List of open inputs
nrun = 1; % enter the number of runs here
jobfile = {'C:\Users\17588\Desktop\Yanchen Wang\dev_projects\PsychBox\code\flair\batch_preproc_structural_job.m'};
jobs = repmat(jobfile, 1, nrun);
inputs = cell(0, nrun);
for crun = 1:nrun
end
spm('defaults', 'FMRI');
spm_jobman('run', jobs, inputs{:});
