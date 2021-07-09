import streamlit as st
import pandas as pd
import numpy as np
import folium as fo
from streamlit_folium import folium_static
import geopandas as gp

df = pd.read_csv('https://raw.githubusercontent.com/Kodchakarn/Infraplus_Assignment/main/Data/data_point.csv')
null_columns = df.columns[df.isnull().any()]
df_null_1 = df[df.isnull().any(axis=1)]
df_null_2 = df[(df['lat'] > 21) | (df['lat'] < 5) | (df['lon']<97) | (df['lon']>106)]
df_null = pd.concat([df_null_1, df_null_2]).drop_duplicates()
df_null = df_null.reset_index(drop=True)

st.title("Assignment Infraplus")
if st.checkbox('Show dataframe'):
    df_null

# set geometry
crs = "EPSG:4326"
geometry = gp.points_from_xy(df_null.lon,df_null.lat)
geo_df  = gp.GeoDataFrame(df_null,crs=crs,geometry=geometry)
# Create Map
longitude = 100.523186
latitude = 13.736717
station_map = fo.Map(
                location = [latitude, longitude], 
                zoom_start = 10)
latitudes = list(df_null.lat)
longitudes = list(df_null.lon)
labels = list(df_null.name)

# Add popup
for lat, lon, label in zip(latitudes, longitudes, labels):
    if np.isnan(lat)!=True and np.isnan(lon)!=True:
        fo.Marker(
          location = [lat, lon], 
          popup = [label,lat,lon],
          icon = fo.Icon(color='black', icon='map-marker')
         ).add_to(station_map)
folium_static(station_map)
