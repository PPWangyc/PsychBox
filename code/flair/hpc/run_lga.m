% Initialize SPM job manager
spm_jobman('initcfg');

% Define paths to your FLAIR and optional reference images
flair_images = {flair_path}; % Add paths as needed
t1_images = {t1_path}; % Ensure matching order and count with FLAIR images
reference_images = {}; % Ensure matching order and count with FLAIR images

% Specify whether to generate HTML reports (1 for yes, 0 for no)
html_report = 1;

% Create a structure to pass to the function
job.data_F2 = flair_images;
job.data_coreg = reference_images; % Can be empty if not using coregistration
job.html_report = html_report;

% Call the function
ps_LST_lga(t1_path,flair_path, threshold);

% Optionally, add additional code to handle outputs, logs, or further processing