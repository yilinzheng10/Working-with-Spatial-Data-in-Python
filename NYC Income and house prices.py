import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points
from scipy.stats import pearsonr

# is there a relationship between the density of trees in a neighborhood and the income of it's residents?

path = r'C:\Users\zheng\OneDrive - Louisiana State University\Documents\1 GSAPP\SMORGASBORD\1 Data\NYC_Citywide_Annualized_Calendar_Sales_Update_20240626.csv'
houses = pd.read_csv(path, dtype={'SALE PRICE': int, 'Latitude': float, 'Longitude': float})


def lat_lng_to_point(data):
    return Point([data['Longitude'], data['Latitude']])

houses['geom'] = houses.apply(lat_lng_to_point, axis=1)
gdf = gpd.GeoDataFrame(houses, geometry='geom', crs='EPSG:4326')

path = r'C:\Users\zheng\OneDrive - Louisiana State University\Documents\1 GSAPP\SMORGASBORD\1 Data\NYC_Borough_Boundary.geojson'
nyc_geo = gpd.read_file(path)

bk = nyc_geo.loc[nyc_geo['BoroName']=='Brooklyn']
bk = bk.to_crs('EPSG:4326')  # Reproject to a projected CRS
bk_houses = gpd.sjoin(gdf, bk)

#filter the data to only have single family homes
mask = bk_houses['BUILDING CLASS CATEGORY']=='01 ONE FAMILY DWELLINGS'
bk_houses = bk_houses.loc[mask]

bk_houses.hist(bins=20);

mask = (bk_houses['SALE PRICE'] > 1e6) & (bk_houses['SALE PRICE'] < 3e6)
bk_houses = bk_houses.loc[mask]

# Plotting boundaries of Manhattan & Brooklyn
ax = nyc_geo.loc[nyc_geo['BoroName'].isin(['Manhattan', 'Brooklyn'])].boundary.plot(
    figsize=(18, 16), linewidth=0.75, color='black'
)

# Draw rings around the centroid of Manhattan (optional)
nyc_geo.loc[nyc_geo['BoroName']=='Manhattan'].boundary.\
    centroid.buffer(0.1).boundary.plot(ax=ax, linestyle='--', color='grey', linewidth=0.75)
nyc_geo.loc[nyc_geo['BoroName']=='Manhattan'].boundary.\
    centroid.buffer(0.15).boundary.plot(ax=ax, linestyle='--', color='grey', linewidth=0.75)
nyc_geo.loc[nyc_geo['BoroName']=='Manhattan'].boundary.\
    centroid.buffer(0.2).boundary.plot(ax=ax, linestyle='--', color='grey', linewidth=0.75)

# Plot individual houses using sales price as color
bk_houses[(bk_houses['SALE PRICE'] > 1e6) & (bk_houses['SALE PRICE'] < 3e6)].plot(
    ax=ax, column='SALE PRICE', legend=True, cmap='Spectral', alpha=0.5, legend_kwds={'shrink': 0.6}
)

# Turn off axis
ax.set_axis_off()

# get just the geometry of Manhattan
mn = nyc_geo.loc[nyc_geo['BoroName']=='Manhattan']

# nearest function to return the closest distance
# .nearest (point, pts), finds the closest pair of points between two geometries: point and pts
def nearest (point, pts): #point (a single geometric point) and pts (a collection of geometric points or shapes)
    return nearest_points(point, pts)[1].distance(point)

# unionize/combines all the Manhattan geometry
mn_pt = mn.geometry.unary_union

# create a new column with the distance for every house in Brooklyn
bk_houses['dis_manhattan'] = bk_houses['geom'].apply(lambda x: nearest(x, mn_pt))

# analyze the relationship between house prices and their distances to Manhattan 
pearsonr(bk_houses['SALE HOUSE'], bk_houses['dist_manhattan'])

# plot scatterplot on matplotlib
plt.scatter(bk_houses['dist_manhattan'], bk_houses['SALE PRICE']);

# conditional masks to constrain the square footage, sale price, year built and ensure there are no commercial units within a house
sqft = bk_houses['GROSS SQUARE FEET'].str.replace(',|- ','').astype(float)

mask1 = (sqft <= 2000) & (sqft >= 1000)
mask2 = (bk_houses['SALE PRICE'] > 1e6) & (bk_houses['SALE PRICE'] < 3e6)
mask4 = bk_houses['COMMERCIAL UNITS'] < 1.
mask5 = bk_houses['YEAR BUILT'] <= 1980

dates = pd.to_datetime(bk_houses['SALE DATE'])
mask3 = (dates< '2019-12-31') & (dates>'2019-01-01')

data = bk_houses[(mask1) & (mask2) & (mask3) & (mask4) & (mask5)]
print(data.shape)

print(pearsonr(data['SALE PRICE'], data['dist_manhattan']))

# define x and y variables used for plotting
x = data['dist_manhattan']
y = data['SALE PRICE']

# set the background color and size
sns.set(rc={'figure.figsize':(14.7,11.27)})
sns.set_style("white")
# create the Seaborn regression plot
# we will use dictionaries to change the line styles of the plot
ax = sns.regplot(x, y, ci=None,
            scatter_kws={
                'color':'orange',
                'edgecolor':'black',
                'alpha':0.75},
           line_kws={
               'color':'red',
               'linestyle':'dashed',
               'linewidth':0.75
           });
# label the x and y axis
plt.xlabel('Distance to Manhattan')
plt.ylabel('Sale price $ (millions)')

# remove the top and right axis
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)