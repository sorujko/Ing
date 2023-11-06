import streamlit as st
st.set_page_config(
    page_title="Dice Roller",
    layout="centered"
)

from random import randint
import random
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.markdown("# Dice Roller")
st.sidebar.header("Dice Roller")
st.sidebar.write("##### Popis:")
st.sidebar.write("""Táto stránka obsahuje 2 inputy - počet hodov
                 a počet kociek , ktoré budú hodené v backende programu
                 a vám sa už len zobrazí výsledok v podobe 3 dvojíc grafov.
                 Prvá reprezentuje súčty hodov, druhá koľkokrát padlo ktoré číslo
                 a tretia koľko padlo párnych(2-4-6) a koľko nepárnych(1-3-5) cifier.
                 Farby reprezentujú danú X hodnotu v oboch stĺpcovh , sú generovane
                 náhodne , niekedy celkom crazy xD.
                 Keď ich náhodou od seba neviete rozoznať , tak re-roll i guess.""")
class Die:
    def __init__(self,num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return randint(1,self.num_sides)

col1, col2 = st.columns(2)
with col1:
    pocet_kociek_1_6 = st.number_input('Počet kociek 1-6:' , min_value=0,max_value=5,step=1 , value=2 ,)
with col2:
    pocet_hodov_1_6 =st.number_input('Počet hodov:' , min_value=1,max_value=10000,step=100 , value = 300)
col1, col2 = st.columns(2)
with col1:
    pocet_kociek_1_4 = st.number_input('Počet kociek 1-4:' , min_value=0,max_value=4,step=1 , value=0 , key='akjl')
with col2:
    pocet_hodov_1_4 =st.number_input('Počet hodov:' , min_value=1,max_value=10000,step=100 , value = 300 , key = 'aazerz')
col1, col2 = st.columns(2)
with col1:
    pocet_kociek_1_8 = st.number_input('Počet kociek 1-8:' , min_value=0,max_value=8,step=1 , value=0 , key='aadhgha')
with col2:
    pocet_hodov_1_8 =st.number_input('Počet hodov:' , min_value=1,max_value=10000,step=100 , value = 300, key = 'aaacvnbaa')
col1, col2 = st.columns(2)
with col1:
    pocet_kociek_1_10 = st.number_input('Počet kociek 1-10:' , min_value=0,max_value=10,step=1 , value=0, key = 'aaaa46345dsa')
with col2:
    pocet_hodov_1_10 =st.number_input('Počet hodov:' , min_value=1,max_value=10000,step=100 , value = 300 , key = 'dsad1414sad')


kocky_1_6=[]
for i in range(pocet_kociek_1_6):
    kocky_1_6.append(Die())
kocky_1_4=[]
for i in range(pocet_kociek_1_4):
    kocky_1_4.append(Die(num_sides=4))
kocky_1_8=[]
for i in range(pocet_kociek_1_8):
    kocky_1_8.append(Die(num_sides=8))
kocky_1_10=[] 
for i in range(pocet_kociek_1_10):
    kocky_1_10.append(Die(num_sides=10))

hody=[]
sucty=[]
parne=0
neparne=0
for i in range(pocet_hodov_1_6):
    sucet=0
    for kocka in kocky_1_6:
        hod=kocka.roll()
        if hod in [2,4,6,8,10]:
            parne+=1
        if hod in [1,3,5,7,9]:
            neparne+=1
        sucet+=hod
        hody.append(hod)
    sucty.append(sucet)

for i in range(pocet_hodov_1_4):
    sucet=0
    for kocka in kocky_1_4:
        hod=kocka.roll()
        if hod in [2,4,6,8,10]:
            parne+=1
        if hod in [1,3,5,7,9]:
            neparne+=1
        sucet+=hod
        hody.append(hod)
    sucty[i]=sucty[i]+sucet

for i in range(pocet_hodov_1_8):
    sucet=0
    for kocka in kocky_1_8:
        hod=kocka.roll()
        if hod in [2,4,6,8,10]:
            parne+=1
        if hod in [1,3,5,7,9]:
            neparne+=1
        sucet+=hod
        hody.append(hod)
    sucty[i]=sucty[i]+sucet

for i in range(pocet_hodov_1_10):
    sucet=0
    for kocka in kocky_1_10:
        hod=kocka.roll()
        if hod in [2,4,6,8,10]:
            parne+=1
        if hod in [1,3,5,7,9]:
            neparne+=1
        sucet+=hod
        hody.append(hod)
    sucty[i]=sucty[i]+sucet
frequencies = []
max_sucet = pocet_kociek_1_10 * 10 +pocet_kociek_1_8 * 8 + pocet_kociek_1_6 * 6 + pocet_kociek_1_4 * 4

min_sucet= (pocet_kociek_1_10 + pocet_kociek_1_8
            + pocet_kociek_1_6 + pocet_kociek_1_4)
for i in range(min_sucet,max_sucet+1):
    frequency= sucty.count(i)
    frequencies.append(frequency)

os_x1=list(range(min_sucet,max_sucet+1))
a=sorted(sucty)
os_y =a[-1]



frequencies2 = []
if pocet_kociek_1_10:
    max_freq2 =10
elif pocet_kociek_1_8:
    max_freq2 =8
elif pocet_kociek_1_6:
    max_freq2 =6
elif pocet_kociek_1_4:
    max_freq2 =4
    
for i in range(1,max_freq2+1):
    frequency=hody.count(i)
    frequencies2.append(frequency)
    


os_x2=list(range(1,max_freq2+1))

#st.write("Súčet jednotlivých hodov",text_align="center")
farby=[]
for item in frequencies:
    farby.append(f'#{random.randrange(256**3):06x}')

fig = make_subplots(rows=1, cols=2 ,specs=[[{'type': 'xy'},{'type': 'domain'}]] )

fig.add_trace(
    go.Bar(x=os_x1, y=frequencies,marker=dict(color=farby), showlegend=False ,name='',hovertemplate='sucet=%{x}, pocet=%{y}') ,
    row=1, col=1
)

fig.add_trace(
    go.Pie(labels=os_x1, values=frequencies,marker=dict(colors=farby),name='',
           hovertemplate='sucet: %{label}<br>pocet: %{value}<br>percento: %{percent}'),
    row=1, col=2
)


fig.update_xaxes(nticks=max_sucet)

fig.update_layout(
    title="Súčet jednotlivých hodov",
    title_x=0.5,
    title_y=0.9
)
st.plotly_chart(fig)

farby=[]
for item in frequencies2:
    farby.append(f'#{random.randrange(256**3):06x}')


#st.write("Súčet 1-6")
fig2 = make_subplots(rows=1, cols=2 ,specs=[[{'type': 'xy'},{'type': 'domain'}]] )

fig2.add_trace(
    go.Bar(x=os_x2, y=frequencies2,marker=dict(color=farby), showlegend=False ,name='',hovertemplate='sucet=%{x}, pocet=%{y}'),
    row=1, col=1
)

fig2.add_trace(
    go.Pie(labels=os_x2, values=frequencies2,marker=dict(colors=farby),name='',
           hovertemplate='padlo: %{label}<br>pocet: %{value}<br>percento: %{percent}'),
    row=1, col=2
)
fig2.update_xaxes(nticks=7)

fig2.update_layout(
    title="Súčet 1-6",
    title_x=0.5,
    title_y=0.9
)

st.plotly_chart(fig2)


farby=[]
for i in range(2):
    farby.append(f'#{random.randrange(256**3):06x}')

#st.write("Súčet párne-nepárne")
fig3 = make_subplots(rows=1, cols=2 ,specs=[[{'type': 'xy'},{'type': 'domain'}]] )

fig3.add_trace(
    go.Bar(x=['parne','neparne'], y=[parne,neparne],marker=dict(color=farby), showlegend=False ,name='',hovertemplate='%{x}, pocet=%{y}'),
    row=1, col=1
)

fig3.add_trace(
    go.Pie(labels=['parne','neparne'], values=[parne,neparne],marker=dict(colors=farby),name='',
           hovertemplate='%{label}<br>pocet: %{value}<br>percento: %{percent}'),
    row=1, col=2
)

fig3.update_layout(
    title="Párne-nepárne",
    title_x=0.5,
    title_y=0.9
)
st.plotly_chart(fig3)