exec(open("../settings/yaml_variables.py").read())
import pickle

# OSM filepaths
osm_processed_fp = f"../../data/OSM/{study_area}/processed/"

osm_graph_fp = osm_processed_fp + "osm_graph.graphml"
osm_graph_simplified_fp = osm_processed_fp + "osm_simplified_graph.graphml"

osm_edges_fp = osm_processed_fp + "osm_edges.parquet"
osm_nodes_fp = osm_processed_fp + "osm_nodes.parquet"
osm_edges_simplified_fp = osm_processed_fp + "osm_edges_simplified.parquet"
osm_nodes_simplified_fp = osm_processed_fp + "osm_nodes_simplified.parquet"

osm_edges_joined_fp = osm_processed_fp + "osm_edges_joined.parquet"
osm_nodes_joined_fp = osm_processed_fp + "osm_nodes_joined.parquet"
osm_edges_simplified_joined_fp = osm_processed_fp + "osm_edges_simplified_joined.parquet"
osm_nodes_simplified_joined_fp = osm_processed_fp + "osm_nodes_simplified_joined.parquet"

osm_grid_fp = osm_processed_fp + "grid.parquet"
osm_intrinsic_grid_fp = (
    f"../../results/OSM/{study_area}/data/grid_results_intrinsic.pickle"
)

osm_intrinsic_fp = f"../../results/OSM/{study_area}/data/intrinsic_analysis.json"

osm_meta_fp = osm_processed_fp + "osm_meta.json"

osm_results_fp = f"../../results/OSM/{study_area}/"

osm_results_static_maps_fp = f"../../results/OSM/{study_area}/maps_static/"
osm_results_inter_maps_fp = f"../../results/OSM/{study_area}/maps_interactive/"
osm_results_plots_fp = f"../../results/OSM/{study_area}/plots/"
osm_results_data_fp = f"../../results/OSM/{study_area}/data/"

# Reference filepaths
ref_processed_fp = f"../../data/REFERENCE/{study_area}/processed/"

ref_graph_fp = ref_processed_fp + "ref_graph.graphml"
ref_graph_simplified_fp = ref_processed_fp + "ref_simplified_graph.graphml"

ref_edges_fp = ref_processed_fp + "ref_edges.parquet"
ref_nodes_fp = ref_processed_fp + "ref_nodes.parquet"
ref_edges_simplified_fp = ref_processed_fp + "ref_edges_simplified.parquet"
ref_nodes_simplified_fp = ref_processed_fp + "ref_nodes_simplified.parquet"

ref_edges_joined_fp = ref_processed_fp + "ref_edges_joined.parquet"
ref_nodes_joined_fp = ref_processed_fp + "ref_nodes_joined.parquet"
ref_edges_simplified_joined_fp = ref_processed_fp + "ref_edges_simplified_joined.parquet"
ref_nodes_simplified_joined_fp = ref_processed_fp + "ref_nodes_simplified_joined.parquet"

ref_grid_fp = ref_processed_fp + "grid.parquet"
ref_intrinsic_grid_fp = (
    f"../../results/REFERENCE/{study_area}/data/grid_results_intrinsic.pickle"
)

ref_intrinsic_fp = f"../../results/REFERENCE/{study_area}/data/intrinsic_analysis.json"

ref_results_fp = f"../../results/REFERENCE/{study_area}/"

ref_results_static_maps_fp = f"../../results/REFERENCE/{study_area}/maps_static/"
ref_results_inter_maps_fp = f"../../results/REFERENCE/{study_area}/maps_interactive/"
ref_results_plots_fp = f"../../results/REFERENCE/{study_area}/plots/"
ref_results_data_fp = f"../../results/REFERENCE/{study_area}/data/"

# COMPARE DATA FILEPATH
compare_processed_fp = f"../../data/COMPARE/{study_area}/processed/"

# COMPARE RESULTS FILEPATHS
compare_results_fp = f"../../results/REFERENCE/{study_area}/"

compare_results_static_maps_fp = f"../../results/COMPARE/{study_area}/maps_static/"
compare_results_inter_maps_fp = f"../../results/COMPARE/{study_area}/maps_interactive/"
compare_results_plots_fp = f"../../results/COMPARE/{study_area}/plots/"
compare_results_data_fp = f"../../results/COMPARE/{study_area}/data/"
