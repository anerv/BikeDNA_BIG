exec(open("../settings/yaml_variables.py").read())
exec(open("../settings/paths.py").read())


assert len(bicycle_nodes) == len(bicycle_nodes.osmid.unique())
assert len(bicycle_edges) == len(bicycle_edges.edge_id.unique())
assert len(bicycle_edges_simplified) == len(bicycle_edges_simplified.edge_id.unique())
assert len(bicycle_nodes_simplified) == len(
    bicycle_nodes_simplified.osmid.unique()
)

assert "infrastructure_length" in bicycle_edges_simplified.columns
assert "length" in bicycle_edges.columns

bicycle_nodes.to_parquet(osm_nodes_fp, index=True)

bicycle_edges.to_parquet(osm_edges_fp, index=True)

bicycle_nodes_simplified.to_parquet(osm_nodes_simplified_fp, index=True)

cols = [
    "edge_id",
    "osmid",
    "length",
    "infrastructure_length",
    "protected",
    "multiedge",
    "bicycle_infrastructure",
    "bicycle_bidirectional",
    "bicycle_geometries",
    "geometry",
]
keep_cols = [c for c in cols if c in bicycle_edges_simplified.columns]

bicycle_edges_simplified["osmid"] = bicycle_edges_simplified["osmid"].astype(str)
bicycle_edges_simplified["osmid"] = bicycle_edges_simplified["osmid"].astype(str)
bicycle_edges_simplified = bicycle_edges_simplified[keep_cols]

bicycle_edges_simplified.to_parquet(osm_edges_simplified_fp, index=True)

osm_nodes_joined.to_parquet(osm_nodes_joined_fp, index=True)

osm_edges_joined.to_parquet(osm_edges_joined_fp, index=True)

osm_nodes_simp_joined.to_parquet(
    osm_nodes_simplified_joined_fp, index=True
)

cols = [
    "edge_id",
    "osmid",
    "length",
    "infrastructure_length",
    "protected",
    "multiedge",
    "bicycle_bidirectional",
    "bicycle_geometries",
    "grid_id",
    "u",
    "v",
    "key",
    "geometry",
]
keep_cols = [c for c in cols if c in osm_edges_simp_joined.columns]

osm_edges_simp_joined["osmid"] = osm_edges_simp_joined["osmid"].astype(str)
osm_edges_simp_joined["osmid"] = osm_edges_simp_joined["osmid"].astype(str)
osm_edges_simp_joined = osm_edges_simp_joined[keep_cols]

osm_edges_simp_joined.to_parquet(
    osm_edges_simplified_joined_fp, index=True
)

print("OSM nodes and edges saved successfully!")

ox.save_graphml(bicycle_graph, osm_graph_fp)
ox.save_graphml(bicycle_graph_simplified, osm_graph_simplified_fp)
print("OSM networks saved successfully!")

# Export grid
grid.to_parquet(osm_grid_fp)
print("OSM grid saved successfully!")
