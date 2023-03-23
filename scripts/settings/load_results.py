import geopandas as gpd
import pickle
import json
import pandas as pd

exec(open("../settings/yaml_variables.py").read())
exec(open("../settings/paths.py").read())

# Load and merge grids with local intrinsic results


# Load grid with results

# osm_intrinsic_grid = gpd.read_parquet(osm_results_data_fp + "osm_intrinsic_grid_results.parquet")
# ref_intrinsic_grid = gpd.read_parquet(ref_results_data_fp + "ref_intrinsic_grid_results.parquet")

# grid = pd.merge(left=osm_intrinsic_grid, right=ref_intrinsic_grid.drop('geometry',axis=1), left_index=True, right_index=True, suffixes=('_osm','_ref'))
# assert len(grid) == len(osm_intrinsic_grid) == len(ref_intrinsic_grid)
# grid['grid_id'] = grid.grid_id_osm

with open(
    f"../../results/OSM/{study_area}/data/grid_results_intrinsic.pickle", "rb"
) as fp:
    osm_intrinsic_grid = pickle.load(fp)

with open(
    f"../../results/REFERENCE/{study_area}/data/grid_results_intrinsic.pickle", "rb"
) as fp:
    ref_intrinsic_grid = pickle.load(fp)

ref_intrinsic_grid.drop("geometry", axis=1, inplace=True)

grid = osm_intrinsic_grid.merge(
    ref_intrinsic_grid, on="grid_id", suffixes=("_osm", "_ref")
)

assert len(grid) == len(osm_intrinsic_grid) == len(ref_intrinsic_grid)

grid_ids = grid.grid_id.to_list()

# Load JSON files with results of intrinsic results

osm_intrinsic_file = open(
    f"../../results/OSM/{study_area}/data/intrinsic_analysis.json"
)

osm_intrinsic_results = json.load(osm_intrinsic_file)

ref_intrinsic_file = open(
    f"../../results/REFERENCE/{study_area}/data/intrinsic_analysis.json"
)

ref_intrinsic_results = json.load(ref_intrinsic_file)


print("Results from intrinsic analyses loaded successfully!")
