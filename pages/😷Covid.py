import geopandas as gpd
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import random
import datetime
# Load your GeoDataFrame
st.set_page_config(layout='wide' , page_title="Covid")
st.title('Covid')
okresy = pd.read_csv('data/covid_data2.csv')
okresy.fillna(0, inplace=True)

today_date = datetime.datetime.now().strftime("%Y-%m-%d")

with open('data/check.txt', 'r') as file:
    file_contents = file.read()
    if today_date in file_contents:
        pass
    else:
        with open('data/check.txt', 'w') as file:
            file.write(today_date)
            okresy['nove_pripady'] = [random.randint(0, 100) for _ in range(len(okresy))]

gdf = gpd.read_file('data/districts.shp', encoding='utf8')
gdf = gpd.GeoDataFrame(gdf, geometry='geometry')
gdf.crs = 'epsg:4326'



# Create a list of colors based on 'nove_pripady' values
num_districts = len(gdf)
colors = []
for i in range(num_districts):
    value = okresy.iloc[i, 2]
    if value == 0:
        color = '#faf0e6'
    elif 1 <= value <= 25:
        color = '#ff7b7b'  
    elif 26 <= value <= 50:
        color = '#ff5252'  
    elif 51 <= value <= 75:
        color = '#ff0000' 
    elif 76 <= value <= 100:
        color = '#a70000' 
    colors.append(color)

# Plot the GeoDataFrame with the custom colormap
ax = gdf.plot(color=colors, edgecolor='black')

annotations = []
for i, row in gdf.iterrows():
    if okresy.iloc[i, 2] > 0:
        if okresy.iloc[i, 0] == 'Košice - okolie':
            x_offset = -0.2  # Adjust the x_offset to move the number to the left
            y_offset = -0.05
            fontsize = 5
            
        else:
            x_offset = 0
            y_offset = 0
            fontsize = 5
        annotation = plt.annotate(okresy.iloc[i, 2], xy=(row.geometry.centroid.coords[0][0] + x_offset,
                                                         row.geometry.centroid.coords[0][1] + y_offset), ha='center', fontsize=fontsize)
        annotations.append(annotation)
okresy.to_csv("data/covid_data2.csv", index=False, encoding='UTF-8-sig')
fig = ax.get_figure()
st.pyplot(fig)
width = 1140  # You can set this to your desired width in pixels
height = 300  # You can set this to your desired height in pixels
st.image('images/okresy.png',use_column_width=True)

