
# Load libraries, settings and data

import os.path
import pickle
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd

import pandas as pd
import evaluation_functions as eval_func
import matching_functions as match_func

ref_edges_simplified = gpd.read_parquet("data/ref_edges_simplified.parquet")
ref_edges_simp_joined = gpd.read_parquet("data/ref_edges_simplified_joined.parquet")
osm_edges_simplified = gpd.read_parquet("data/ref_edges_simplified.parquet")
osm_edges_simp_joined = gpd.read_parquet("data/ref_edges_simplified_joined.parquet")

ref_grid = gpd.read_parquet("data/ref_grid.parquet")
osm_grid = gpd.read_parquet("data/osm_grid.parquet")

grid = pd.merge(left=osm_grid, right=ref_grid, left_index=True, right_index=True, suffixes=('_osm','_ref'))
assert len(grid) == len(osm_grid) == len(ref_grid)

# settings
study_crs = "EPSG:25832"
study_area = 'dk'
reference_name = 'GeoDanmark'


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

buffer_matches = match_func.overlay_buffer(
    reference_data=ref_segments,
    osm_data=osm_segments,
    ref_id_col="seg_id_ref",
    osm_id_col="seg_id",
    dist=buffer_dist,
)


# final matches
segment_matches = match_func.find_matches_from_buffer(
    buffer_matches=buffer_matches,
    osm_edges=osm_segments,
    reference_data=ref_segments,
    angular_threshold=angular_threshold,
    hausdorff_threshold=hausdorff_threshold,
)

matches_fp = "results/segment_matches_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.pickle"

with open(matches_fp, "wb") as f:
    pickle.dump(segment_matches, f)


# Summarize feature matching results
osm_matched_ids, osm_undec = match_func.summarize_feature_matches(
    osm_segments, segment_matches, "seg_id", "osmid", osm=True
)

ref_matched_ids, ref_undec = match_func.summarize_feature_matches(
    ref_segments, segment_matches, "seg_id_ref", "edge_id", osm=False
)

protection_level_comparison = match_func.update_osm(
    osm_segments,
    osm_edges_simplified,
    segment_matches,
    "protected",
    "edge_id",
    "seg_id",
)

osm_matched = osm_edges_simp_joined.loc[
    osm_edges_simp_joined.edge_id.isin(osm_matched_ids)
]

ref_matched = ref_edges_simp_joined.loc[
    ref_edges_simp_joined.edge_id.isin(ref_matched_ids)
]

# Count features in each grid cell
data = [osm_matched, ref_matched]
labels = ["osm_matched", "ref_matched"]

for data, label in zip(data, labels):

    df = eval_func.count_features_in_grid(data, label)

    grid = eval_func.merge_results(grid, df, "left")

    df = eval_func.length_of_features_in_grid(data, label)

    grid = eval_func.merge_results(grid, df, "left")

# Get length of features in each grid cell
data = [osm_edges_simp_joined, ref_edges_simp_joined]
labels = ["osm", "ref"]

for data, label in zip(data, labels):

    df = eval_func.length_of_features_in_grid(data, label)

    grid = eval_func.merge_results(grid, df, "left")

# Compute pct matched
grid["pct_matched_osm"] = (
    grid["count_osm_matched"] / grid["count_osm_simplified_edges"] * 100
)
grid["pct_matched_ref"] = (
    grid["count_ref_matched"] / grid["count_ref_simplified_edges"] * 100
)

# Compute unmatched
grid.loc[
    (grid.count_osm_simplified_edges.notnull()) & (grid.count_osm_matched.isnull()),
    ["count_osm_matched"],
] = 0
grid.loc[
    (grid.count_ref_simplified_edges.notnull()) & (grid.count_ref_matched.isnull()),
    ["count_ref_matched"],
] = 0
grid.loc[
    (grid.count_osm_simplified_edges.notnull()) & (grid.pct_matched_osm.isnull()),
    ["pct_matched_osm"],
] = 0
grid.loc[
    (grid.count_ref_simplified_edges.notnull()) & (grid.pct_matched_ref.isnull()),
    ["pct_matched_ref"],
] = 0

grid.loc[
    (grid.count_osm_simplified_edges.notnull()) & (grid.length_osm_matched.isnull()),
    ["length_osm_matched"],
] = 0
grid.loc[
    (grid.count_ref_simplified_edges.notnull()) & (grid.length_ref_matched.isnull()),
    ["length_ref_matched"],
] = 0

grid["count_osm_unmatched"] = grid.count_osm_simplified_edges - grid.count_osm_matched
grid["count_ref_unmatched"] = grid.count_ref_simplified_edges - grid.count_ref_matched

grid["length_osm_unmatched"] = grid.length_osm - grid.length_osm_matched
grid["length_ref_unmatched"] = grid.length_ref - grid.length_ref_matched

# Compute pct unmatched
grid["pct_unmatched_osm"] = (
    grid["count_osm_unmatched"] / grid["count_osm_simplified_edges"] * 100
)
grid["pct_unmatched_ref"] = (
    grid["count_ref_unmatched"] / grid["count_ref_simplified_edges"] * 100
)

grid.loc[grid.pct_matched_osm == 100, "pct_unmatched_osm"] = 0
grid.loc[grid.pct_matched_ref == 100, "pct_unmatched_ref"] = 0

grid.to_parquet("results/grid_fm.parquet")