# Instructions for running the feature matching on a High Performance Computing Cluster

These instructions assumes a HPC using [SLURM](<https://slurm.schedmd.com/overview.html>) scheduling.

Adapt instructions to your own HPC as necessary.

## Setting up the conda environment

```bash
module load Anaconda3
eval "$(conda shell.bash hook)"
conda config --prepend channels conda-forge
conda create -n bikedna_min --strict-channel-priority geopandas pyarrow pyyaml
```

or alternatively, upload the `environment_minimal.yml` file in the `feature_matching_hpc` folder:

```bash
module load Anaconda3
eval "$(conda shell.bash hook)"
conda env create --file=environment_minimal.yml
```

## Create subfolders and copy files to folder

- Navigate to the `feature_matching_hpc` folder in a terminal and run:

```bash
python setup_hpc_folders.py
```

## Upload files

Use for example scp to upload the `feature_matching_hpc` folder to the HPC:

```bash
scp -r /Users/myuser/../bikedna_denmark/feature_matching_hpc user@host:/home/user
```
<!-- scp -r /Users/anev/Dropbox/ITU/repositories/bikedna_denmark/feature_matching_hpc anev@hpc.itu.dk:/home/anev -->

Navigate to the `feature_matching_hpc` folder on the HPC and run:

```bash
sbatch scripts/fm.job
```

Once the job is completed:

- download the data in the `results` folder and place them in `bikedna_denmark/feature_matching_hpc/results/` on your own machine
- download the data in the `processed` folder and place them in `bikedna_denmark/feature_matching_hpc/processed/` on your own machine
- navigate to the folder `feature_matching_hpc` on your own machine, activate the conda environment, and run:

```bash
python export_hpc_results.py
```

- run the `3b_extrinsic_analyis_feature_matching` notebook as normal to summarize results, analyze local success rates, produce plots, etc.
