import geopandas as gpd
import pandas as pd
import pyarrow.parquet as pq
from shapely.geometry import Point
# %%
def dfToGdf(df, lon, lat, crs='EPSG:4326'):
  '''
    df: pandas dataframe
    lon: longitude column name
    lat: latitude column name
    crs: EPSG code or similar coordinate reference system
  '''
  return gpd.GeoDataFrame(
    df.drop([lon, lat], axis=1),
    crs=crs,
    geometry=[Point(xy) for xy in zip(df[lon], df[lat])])

# %%
raw = pd.read_csv("./us-post-offices.csv")
gdf = dfToGdf(raw.query('Coordinates == True'), 'Longitude', 'Latitude')
# %%
columns_we_want = [
    "Name",
    "State",
    "Established",
    "Discontinued",
    "Duration",
    "GNIS.OrigName",
    "GNIS.ELEV_IN_M",
    "geometry",
]

cleaned = gdf[columns_we_want]
cleaned.rename(columns={
    "GNIS.OrigName": "OriginalName",
    "GNIS.ELEV_IN_M": "EvelationMeters"
}, inplace=True)
#%% 
cleaned.to_parquet('./post_offices.parquet')