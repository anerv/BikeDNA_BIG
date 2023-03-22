# Run this file while in the hpc folder

import os
import yaml
import shutil

with open(r"config.yml") as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area = parsed_yaml_file["study_area"]

study_area_folder = f"{study_area}/"

if not os.path.exists(study_area_folder):
    os.mkdir(study_area_folder)

folders = [f"{study_area}/data/", f"{study_area}/processed", f"{study_area}/results","scripts/src"]

for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)

copy_files = {
    f"../data/OSM/{study_area}/processed/grid.parquet":f"{study_area}/data/osm_grid.parquet",
    f"../data/REFERENCE/{study_area}/processed/grid.parquet":f"{study_area}/data/ref_grid.parquet",
    f"../data/REFERENCE/{study_area}/processed/ref_edges_simplified.parquet":f"{study_area}/data/ref_edges_simplified.parquet",
    f"../data/REFERENCE/{study_area}/processed/ref_edges_simplified_joined.parquet":f"{study_area}/data/ref_edges_simplified_joined.parquet",
    f"../data/OSM/{study_area}/processed/osm_edges_simplified.parquet":f"{study_area}/data/osm_edges_simplified.parquet",
    f"../data/OSM/{study_area}/processed/osm_edges_simplified_joined.parquet":f"{study_area}/data/osm_edges_simplified_joined.parquet",
    "../src/matching_functions.py":"scripts/src/matching_functions.py",
    "../config.yml":"config.yml"
}
    
for src, dst in copy_files.items():

    shutil.copyfile(src, dst)
