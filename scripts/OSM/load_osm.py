#%%
import pyrosm
import yaml
import osmnx as ox
import networkx as nx
import pandas as pd
import geopandas as gpd
import json
from src import db_functions as dbf
import pickle
from src import simplification_functions as sf
from src import graph_functions as gf
from timeit import default_timer as timer
import os.path

#%%
# with open(r'../config.yml') as file:

#     parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

#     osm_fp = parsed_yaml_file['osm_fp']

#     ref_id_col = parsed_yaml_file['geodk_id_col']

#     crs = parsed_yaml_file['CRS']

# print('Settings loaded!')

#%%
# Creating OSM object
osm = pyrosm.OSM("../data/raw/denmark-latest.osm.pbf")

extra_attr = [
    "surface",
    "cycleway:left",
    "cycleway:right",
    "cycleway:both",
    "cycleway:width",
    "cycleway:oneway",
    "maxspeed",
    "cycleway:surface",
]

#%%
start = timer()

print("Creating edge and node datasets...")
nodes, edges = osm.get_network(
    nodes=True, network_type="cycling", extra_attributes=extra_attr
)
end = timer()
print((end - start) / 60)


#%%
# Filter out edges with irrelevant highway types
# unused_highway_values = [
#     "abandoned",
#     "planned",
#     "proposed",
#     "construction",
#     "disused",
#     "elevator",
#     "platform",
#     "bus_stop",
#     "step",
#     "steps",
#     "corridor",
#     "raceway",
#     "bus_guideway",
#     "rest_area",
#     "razed",
#     "layby",
#     "skyway",
#     "su",
# ]

# org_len = len(edges)
# edges = edges.loc[~edges.highway.isin(unused_highway_values)]

# # Filter out pedestrian edges
# pedestrian_edges = edges.loc[
#     (edges.highway.isin(["footway", "pedestrian"]))
#     & (
#         ~edges.bicycle.isin(
#             ["allowed", "ok", "designated", "permissive", "yes", "destination"]
#         )
#     )
# ]
# edges.drop(pedestrian_edges.index, inplace=True)

# new_len = len(edges)

# print(f"{org_len - new_len} edges where removed")

# # Filter unused nodes
# node_id_list = list(set(edges.u.to_list() + edges.v.to_list()))
# nodes = nodes.loc[nodes.id.isin(node_id_list)]

#%%
# Drop unnecessary cols
drop_cols = [
    "overtaking",
    "psv",
    "ref",
    "int_ref",
    "construction",
    "proposed",
    "timestamp",
    "version",
    "osm_type",
    "passing_places",
    "area",
    "footway",
    "foot",
    "junction",
    "path",
    "sidewalk",
    "tracktype",
    "turn",
    "tags",
    "lanes",
    "busway",
    "motorroad",
    "motor_vehicle",
    "motorcar",
    "name",
    "service",
]

drop_cols = [c for c in drop_cols if c in edges.columns]
edges.drop(
    drop_cols,
    axis=1,
    inplace=True,
)

nodes_drop_cols = ["tags", "timestamp", "version", "changeset"]
nodes_drop_cols = [c for c in nodes_drop_cols if c in nodes.columns]

nodes.drop(
    nodes_drop_cols,
    axis=1,
    inplace=True,
)

#%%
# Clean col names


def clean_col_names(df):

    """
    Remove upper-case letters and : from data with OSM tags
    Special characters like ':' can for example break with pd.query function

    Arguments:
        df (df/gdf): dataframe/geodataframe with OSM tag data

    Returns:
        df (df/gdf): the same dataframe with updated column names
    """

    df.columns = df.columns.str.lower()

    df_cols = df.columns.to_list()

    new_cols = [c.replace(":", "_") for c in df_cols]

    df.columns = new_cols

    return df


edges = clean_col_names(edges)

#%%
# Get cycling edges

bicycle_infrastructure_queries = [
    "highway == 'cycleway'",
    "cycleway in ['lane','track','opposite_lane','opposite_track','designated','crossing']",
    "cycleway_left in ['lane','track','opposite_lane','opposite_track','designated','crossing']",
    "cycleway_right in ['lane','track','opposite_lane','opposite_track','designated','crossing']",
    "cycleway_both in ['lane','track','opposite_lane','opposite_track','designated','crossing']",
]

edges["bicycle_infrastructure"] = "no"

for q in bicycle_infrastructure_queries:

    try:
        osm_filtered = edges.query(q)

    except Exception:
        print("Exception occured when quering with:", q)
        print("Please check if the columns used in the query are present in the data")

    edges.loc[osm_filtered.index, "bicycle_infrastructure"] = "yes"

edges.bicycle_infrastructure.value_counts()

bicycle_edges = edges.loc[edges.bicycle_infrastructure == "yes"].copy()

#%%
# Get bicycle nodes
bicycle_nodes_id = set(bicycle_edges.u.to_list() + bicycle_edges.v.to_list())

bicycle_nodes = nodes.loc[nodes.id.isin(bicycle_nodes_id)]

#%%
# Create unique ids
assert len(bicycle_nodes.id.unique()) == len(bicycle_nodes)

bicycle_edges["edge_id"] = bicycle_edges.index

assert len(bicycle_edges.edge_id.unique()) == len(bicycle_edges)

#%%
# Save data
# bicycle_edges.to_parquet("../data/processed/bicycle_edges.parquet")
# bicycle_nodes.to_parquet("../data/processed/bicycle_nodes.parquet")
#%%
# bicycle_edges_min = bicycle_edges[["geometry", "u", "v", "edge_id", "oneway"]].copy()

#%%
# Create networkx graph
start = timer()

G = osm.to_graph(bicycle_nodes, bicycle_edges, graph_type="networkx", retain_all=True)

end = timer()
print((end - start) / 60)

#%%
# Save graph
with open("../data/osm_pyrosm_graph", "wb") as handle:
    pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL)

#%%
# # Load graph
# with open("../data/osm_pyrosm_graph", "rb") as input_file:
#     G = pickle.load(input_file)

# bicycle_edges = gpd.read_parquet("../data/processed/bicycle_edges.parquet")

# bicycle_nodes = gpd.read_parquet("../data/processed/bicycle_nodes.parquet")

#%%


def update_edge_data(G, attr, org_value, new_value, di=True):

    """
    Function for updating the edge data values for a networkx graph based on existing edge data value.
    For digraphs, only edges with key 0 are updated (it is assumed that the graph will be converted to undirected later on)
    Updates graph in place!

    Argumets:
        G (networkx graph): graph which edge data will be updated
        attr (str): name of edge attribute to update
        org_value (undefined): original value of edge attribute. Used to find edges to update
        new_value (undefined): new value
        di(boolean): whether the graph is a digraph or not (influences how the graph edge data is accessed)

    Returns
    -------
    None
    """

    if di:
        for n1, n2, d in G.edges(data=True):
            if d[attr] == org_value:
                G[n1][n2][0][attr] = new_value

    else:
        for n1, n2, d in G.edges(data=True):
            if d[attr] == org_value:
                G[n1][n2][attr] = new_value

    return None


#%%
# Fill na/None values for simplification
gf.update_edge_data(G, "cycleway", None, "unknown")
gf.update_edge_data(G, "cycleway_right", None, "unknown")
gf.update_edge_data(G, "cycleway_left", None, "unknown")
gf.update_edge_data(G, "cycleway_both", None, "unknown")
gf.update_edge_data(G, "cycleway_surface", None, "unknown")
gf.update_edge_data(G, "bicycle_road", None, "unknown")
gf.update_edge_data(G, "maxspeed", None, "unknown")
gf.update_edge_data(G, "lit", None, "unknown")
gf.update_edge_data(G, "surface", None, "unknown")
gf.update_edge_data(G, "bicycle", None, "unknown")
# gf.update_edge_data(G, "cyclestreet", None, "unknown")
gf.update_edge_data(G, "access", None, "unknown")
#%%
# Convert to index format used by osmnx
ox_nodes, ox_edges = ox.graph_to_gdfs(G)
# Remove geometry attribute (required by simplification function)
# for n1, n2, d in G.edges(data=True):
#         d.pop('geometry', None)

ox_edges.drop("geometry", axis=1, inplace=True)
G_ox = ox.graph_from_gdfs(ox_nodes, ox_edges)

#%%
# TODO
# Define protected/unprotected, geometry type etc

# Define whether bicycle infrastructure is in both or one direction and whether it is one- or bidirectional

# Define whether bicycle infrastructure is in both or one direction and whether it is one- or bidirectional
bicycle_edges = eval_func.simplify_bicycle_tags(bicycle_edges)

for key, value in bicycle_edges.bicycle_bidirectional.value_counts().items():
    perc = np.round(100 * value / len(bicycle_edges), 2)
    print(
        f"Edges where 'bicycle_bidirectional' is {key}: {value} out of {len(bicycle_edges)} ({perc}%)"
    )
print("\n")

for key, value in bicycle_edges.bicycle_geometries.value_counts().items():
    perc = np.round(100 * value / len(bicycle_edges), 2)
    print(
        f"Edges where the geometry type is '{key}': {value} out of {len(bicycle_edges)} ({perc}%)"
    )
print("\n")

bicycle_bidirectional_dict = bicycle_edges["bicycle_bidirectional"].to_dict()
nx.set_edge_attributes(
    bicycle_graph, bicycle_bidirectional_dict, "bicycle_bidirectional"
)

bicycle_geometries_dict = bicycle_edges["bicycle_geometries"].to_dict()
nx.set_edge_attributes(bicycle_graph, bicycle_geometries_dict, "bicycle_geometries")

# Classify edges as protected or unprotected
bicycle_edges = eval_func.define_protected_unprotected(
    bicycle_edges, osm_bicycle_infrastructure_type
)

# Set edges attributes for column protected
bicycle_protected_dict = bicycle_edges["protected"].to_dict()
nx.set_edge_attributes(bicycle_graph, bicycle_protected_dict, "protected")

for key, value in bicycle_edges.protected.value_counts().items():
    perc = np.round(100 * value / len(bicycle_edges), 2)
    print(
        f"Edges where the protection level is '{key}': {value} out of {len(bicycle_edges)} ({perc}%)"
    )
print("\n")

# Simplify bicycle network
bicycle_graph_simplified = simp_func.simplify_graph(
    bicycle_graph,
    attributes=[
        "bicycle_infrastructure",
        "bicycle_bidirectional",
        "bicycle_geometries",
        "protected",
    ],
    remove_rings=False,
)

#%%

from src import simplification_functions

# Simplify grap # TODO: add protected etc. to attributes
G_sim = sf.simplify_graph(G_ox)

#%%
# Simplify grap
G_sim = sf.simplify_graph(
    G_ox,
    attributes=[
        "highway",
        "cycleway",
        "cycleway:right",
        "cycleway:left",
        "cycleway:both",
        "bicycle_road",
        "maxspeed",
        "lit",
        "surface",
        "cycleway_surface",
        "bicycle",
        "cyclestreet",
        "access",
    ],
)

#%%
# Get undirected
G_sim_un = ox.get_undirected(G_sim)
#%%
start = timer()

G_un = ox.get_undirected(G)
end = timer()
print((end - start) / 60)

#%%
