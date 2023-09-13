<p align="center"><img src="images/BikeDNA_logo.svg" width="50%" alt="BikeDNA logo"/></p>

# BikeDNA: Bicycle Infrastructure Data & Network Assessment

This is the repository of a **version of BikeDNA optimized for dealing with analysis of large areas/large data sets**. BikeDNA is a tool for assessing the quality of [OpenStreetMap (OSM)](https://www.openstreetmap.org/) and other bicycle infrastructure data sets in a reproducible way. It provides planners, researchers, data maintainers, cycling advocates, and others who work with bicycle networks a detailed, informed overview of data quality in a given area.

The original version of BikeDNA lives here: <https://github.com/anerv/BikeDNA>

For an example, see the branch 'denmark_analysis', which contains notebooks with an analysis of bicycle infrastructure data from OpenStreetMap and GeoDanmark for all of Denmark.
Due to limitations on file sizes, the branch only contains the notebooks and not input data or exported results. For a full reproducible setup, see [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8340383.svg)](https://doi.org/10.5281/zenodo.8340383).

For further details and general instructions, see the [README for the original version](https://github.com/anerv/BikeDNA/blob/main/README.md).

## Adaptations for larger data sets

The version of BikeDNA adapted for larger areas has 5 main adaptations:

* OSM data are loaded using Pyrosm. Once the [folder setup](https://github.com/anerv/BikeDNA/blob/main/README.md#set-up-the-folder-structure) has been completed, download an OSM pbf file using e.g. [Geofabrik](<http://download.geofabrik.de/>), place it in the `data>OSM>'my_study_area'>raw` folder, and update the filepath in `1a_initialize_osm.ipynb` to match.
* Edge and node data sets are mostly saved as [geoparquet](<https://geoparquet.org/>) instead of geopackage.
* The grid used for localized analysis is constructed using H3 (specify the desired resolution [H3 resolution](<https://h3geo.org/docs/core-library/restable#cell-counts>) in the `config.yml`).
* To speed up the execution of the notebooks, plotting maps is optional (set `plot_static_maps` and `plot_interactice_maps` to `True` in the beginning of each notebook to plot the maps).
* A workflow for doing the heavy part of the feature matching in notebook 3b on a HPC (high performance cluster) has been added: [HPC instructions](<https://github.com/anerv/bikedna_denmark/blob/main/feature_matching_hpc/hpc_instructions.md>).

Despite these efforts, most of the notebooks can still take several hours to complete, depending on the size of the input data (testeed on macOS 13.2.1 with 2,6 GHz 6-Core Intel Core i7 and 16 GB RAM).

Many of the plots were originally developed for significantly smaller geographical areas. Results might thus be better explored visually using e.g. QGIS or other tools suited for rendering large geospatial data sets.

## Conda environment

Follow the [installation instructions](<https://github.com/anerv/BikeDNA#create-python-conda-environment>) for BikeDNA, but using the environment file from this repository: `environment_minimal.yml`.

## Get in touch

Do you have any suggestions for additional metrics or ways to improve the analysis?
Reach us at <anev@itu.dk> (Ane Rahbek Vierø) or <anvy@itu.dk> (Anastassia Vybornova).

## Data & Licenses

**Our code is free to use and repurpose under the [AGPL 3.0 license](https://www.gnu.org/licenses/agpl-3.0.html).**

The repository includes test data from the following sources:

### OpenStreetMap

© OpenStreetMap contributors  
License: [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/)

### GeoDanmark

Contains data from GeoDanmark (retrieved spring 2022)
© SDFI (Styrelsen for Dataforsyning og Infrastruktur og Danske kommuner)  
License: [GeoDanmark](https://www.geodanmark.dk/wp-content/uploads/2022/08/Vilkaar-for-brug-af-frie-geografiske-data_GeoDanmark-grunddata-august-2022.pdf)

## Credits

Development of BikeDNA was supported by the Danish Road Directorate.

Logo by Katrin Geistler(luftlinie / design & grafik).
