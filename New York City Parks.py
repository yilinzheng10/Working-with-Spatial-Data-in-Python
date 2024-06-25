import pandas as pd
import geopandas as gpd
import osmnx

# Load GeoPandas
path = r'C:\Users\zheng\OneDrive - Louisiana State University\Documents\1 GSAPP\SMORGASBORD\1 Data\NYC Planimetric Database_ Open Space (Parks)_20240625.geojson'
gdf = gpd.read_file(path)

# select subset of columns to display
columns_of_interest = ['park_name', 'landuse', 'shape_area', 'geometry']
# .head display rows
gdf[columns_of_interest].head()

# boolean Series where each element is True if the corresponding entry in 'parknum' contains 'M', and False if 'na' (N/A).
mask = gdf['parknum'].str.contains('M', na = False)
gdf[mask].plot()

# Create a condition that looks for rows with the source ID of Propspect Park
mask = gdf['source_id'] == '19495000142.0'

# use the mask to filter rows GeoDataFrame
prospect_park = gdf[mask]

# retrieve the polygon from the geometry column
# (value returns a list so we select the first item)
polygon = prospect_park['geometry'].values[0]

# use OSMNX to query OpenStreetMap and download a road network
gov_island = osmnx.graph_from_place("Governors Island, New York, United States")
osmnx.plot_graph(gov_island)