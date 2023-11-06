import pandas as pd
import numpy as np
import requests as req
import streamlit as st

st.set_page_config(layout='wide' , page_title="War")
st.title('War')
data = req.get('https://russian-casualties.in.ua/api/v1/data/json/daily')
data = data.json()
legend = data['legend']
data = data['data']



# Slovak translations
slovak_translations = {
    "tanks": "Tanky",
    "apv": "Obrnené vozidlá",
    "artillery": "Delostrelecké Systémy",
    "mlrs": "Vícehlavňový Raketomet",
    "aaws": "Protivzdušné Obranné Systémy",
    "aircraft": "Lietadlá",
    "helicopters": "Vrtuľníky",
    "uav": "Bezpilotné lietadlá",
    "vehicles": "Vozidlá",
    "boats": "Lode",
    "se": "Špeciálne vybavenie",
    "missiles": "riadené strely",
    "personnel": "Personál",
    "captive": "Zajatci"
}


for key, original_value in legend.items():
    legend[key] = {
        "original": original_value,
        "slovak_translation": slovak_translations[key]
    }

on = st.toggle('Zobraziť vysvetlivky')
if on:
    legend

df = pd.DataFrame(data).transpose()
df.reset_index(level=0, inplace=True)
df.rename(columns={'index': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])

start_date = df.iloc[0,0]
end_date = df.iloc[-1,0]

start = st.date_input('Pociatocny datum' , value = start_date , min_value= start_date , max_value=end_date, key = 'eskeree')
end = st.date_input('Konecny datum', value = end_date , min_value=start_date , max_value=end_date , key = 'adsakjhkjh')

start = pd.to_datetime(start)
end = pd.to_datetime(end)


mask = (df['Date'] >= start) & (df['Date'] <= end)

result_df = df.loc[mask]

personnel_sum = result_df['personnel'].sum()
result_df = result_df.drop(columns=['Date', 'personnel'])

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

column_sums = result_df.sum()
st.markdown(f'Medzi zlovenými dátumami prišlo o život :red[{personnel_sum}] ruských vojakov')

fig = make_subplots(rows=1, cols=2 ,
                specs=[[{'type': 'xy'},{'type': 'domain'}]] )

fig.add_trace(
    go.Bar(x=column_sums.index, y=column_sums, 
           showlegend=False ,name='',hovertemplate='technika=%{x}, pocet strat=%{y}') ,
    row=1, col=1
)
fig.add_trace(
    go.Pie(labels=column_sums.index, values=column_sums,name='',
           hovertemplate='technika: %{label}<br>pocet strat: %{value}<br>percento: %{percent}'),
        row=1, col=2
)


fig.update_xaxes(nticks=13)

fig.update_layout(
    title="Straty ruskej armády",
    title_x=0.35,
    title_y=0.9
)
st.plotly_chart(fig, use_container_width=True)