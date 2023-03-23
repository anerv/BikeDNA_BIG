# Load libraries, settings and data

debug = False

import os.path
import pickle
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import pandas as pd
import yaml

from src import matching_functions as match_func

with open(r"../config.yml") as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    study_area = parsed_yaml_file["study_area"]
    study_crs = parsed_yaml_file["study_crs"]
    reference_name = parsed_yaml_file["reference_name"]

path = f"../{study_area}"

ref_edges_simplified = gpd.read_parquet(path+"/data/ref_edges_simplified.parquet")
ref_edges_simp_joined = gpd.read_parquet(path+"/data/ref_edges_simplified_joined.parquet")
osm_edges_simplified = gpd.read_parquet(path+"/data/osm_edges_simplified.parquet")
osm_edges_simp_joined = gpd.read_parquet(path+"/data/osm_edges_simplified_joined.parquet")

ref_grid = gpd.read_parquet(path+"/data/ref_grid.parquet")
osm_grid = gpd.read_parquet(path+"/data/osm_grid.parquet")

grid = pd.merge(left=osm_grid, right=ref_grid.drop('geometry',axis=1), left_index=True, right_index=True, suffixes=('_osm','_ref'))
assert len(grid) == len(osm_grid) == len(ref_grid)
grid['grid_id'] = grid.grid_id_osm


# Define feature matching user settings
segment_length = 10  # The shorter the segments, the longer the matching process will take. For cities with a gridded street network with streets as straight lines, longer segments will usually work fine
buffer_dist = 15
hausdorff_threshold = 17
angular_threshold = 30

for s in [segment_length, buffer_dist, hausdorff_threshold, angular_threshold]:
    assert isinstance(s, int) or isinstance(s, float), print(
        "Settings must be integer or float values!"
    )

osm_segments = match_func.create_segment_gdf(
    osm_edges_simplified, segment_length=segment_length
)
osm_segments.rename(columns={"osmid": "org_osmid"}, inplace=True)
osm_segments["osmid"] = osm_segments[
    "edge_id"
]  # Because matching function assumes an id column names osmid as unique id for edges

osm_segments.set_crs(study_crs, inplace=True)
osm_segments.dropna(subset=["geometry"], inplace=True)

ref_segments = match_func.create_segment_gdf(
    ref_edges_simplified, segment_length=segment_length
)
ref_segments.set_crs(study_crs, inplace=True)
ref_segments.rename(columns={"seg_id": "seg_id_ref"}, inplace=True)
ref_segments.dropna(subset=["geometry"], inplace=True)

print('Segments created!')

osm_segments.to_parquet(path+f"/processed/osm_segments_{segment_length}.parquet")
ref_segments.to_parquet(path+f"/processed/ref_segments_{segment_length}.parquet")

buffer_matches = match_func.overlay_buffer(
    reference_data=ref_segments,
    osm_data=osm_segments,
    ref_id_col="seg_id_ref",
    osm_id_col="seg_id",
    dist=buffer_dist,
)

print('Buffer matches found!')

buffer_matches.to_parquet(path+f"/results/buffer_matches_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.parquet")

# final matches
segment_matches = match_func.find_matches_from_buffer(
    buffer_matches=buffer_matches,
    osm_edges=osm_segments,
    reference_data=ref_segments,
    angular_threshold=angular_threshold,
    hausdorff_threshold=hausdorff_threshold,
)

matches_fp = path+f"/results/segment_matches_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.pickle"

with open(matches_fp, "wb") as f:
    pickle.dump(segment_matches, f)

print("Segment matches found!")

# Summarize feature matching results
osm_matched_ids, osm_undec = match_func.summarize_feature_matches(
    osm_segments, segment_matches, "seg_id", "osmid", osm=True
)

ref_matched_ids, ref_undec = match_func.summarize_feature_matches(
    ref_segments, segment_matches, "seg_id_ref", "edge_id", osm=False
)

osm_matched_ids_fp = path + f"/results/osm_matched_ids_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.pickle"
ref_matched_ids_fp = path + f"/results/ref_matched_ids_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.pickle"

osm_undec_ids_fp = path + f"/results/osm_undec_ids_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.pickle"
ref_undec_ids_fp = path + f"/results/ref_undec_ids_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.pickle"

with open(osm_matched_ids_fp, "wb") as fp:   
    pickle.dump(osm_matched_ids, fp) 

with open(ref_matched_ids_fp, "wb") as fp:   
    pickle.dump(ref_matched_ids, fp) 

with open(osm_undec_ids_fp, "wb") as fp:   
    pickle.dump(osm_undec, fp) 

with open(ref_undec_ids_fp, "wb") as fp:   
    pickle.dump(ref_undec, fp)

print("Summary of segments matches completed. Ids of matched features have been saved.")
