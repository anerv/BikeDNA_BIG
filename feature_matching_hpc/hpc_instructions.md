# Instructions for running the feature matching on a High Performance Cluster

Adapt instructions to your own HPC as necessary.

## Setting up the conda environment

```
module load Anaconda3
eval "$(conda shell.bash hook)"
conda config --prepend channels conda-forge
conda create -n bikedna_min --strict-channel-priority geopandas pyarrow pyyaml
```

or alternatively, upload the `environment_minimal.yml` file in the `feature_matching_hpc` folder:

```
module load Anaconda3
eval "$(conda shell.bash hook)"
conda env create --file=environment_minimal.yml
```

### Upload data

scp -r /Users/anev/Dropbox/ITU/repositories/bikedna_denmark/bikedna_hpc anev@hpc.itu.dk:/home/anev

- create new hpc folder and upload hpc folder to hpc
- install pyaml in env
- test run
- try export

- create conda env on cluster using minimam env file
- navigate to hpcbikedna folder and run setup_hpc_folders.py
- upload hpcbikedna folder, navigate to it and run sbatch scripts/fm.job
- once completeded, download data in results folder to bikednahpc results folder and run export_hpc_results.py
- use the 3b notebook to inspect results, export summmary results, make plots etc.
