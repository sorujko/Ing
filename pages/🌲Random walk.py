import streamlit as st
import matplotlib.pyplot as plt
from random import choice
import random



class Randomwalk:
    
    def __init__(self , pocet_krokov=30, krok=list(range(5)) , strana_lesa=20):
        self.pocet_krokov=pocet_krokov
        self.krok=krok
        self.strana_lesa=strana_lesa
        self.vysledok='STRATILI STE SA V LESE!!'

        self.x_values = [0]
        self.y_values = [0]
        
    def fill_walk(self):
        
        while len(self.x_values) < self.pocet_krokov + 1:
            
            x_direction = choice([-1,1])
            x_distance = choice(self.krok)
            x_step = x_direction * x_distance

            y_direction = choice([-1,1])
            y_distance = choice(self.krok)
            y_step = y_direction * y_distance

            if x_step==0 and y_step ==0:
                continue

            x=self.x_values[-1] +x_step
            y=self.y_values[-1] + y_step

            

            self.x_values.append(x)
            self.y_values.append(y)

            if self.x_values[-1]<-self.strana_lesa or self.x_values[-1] > self.strana_lesa or self.y_values[-1]>self.strana_lesa or self.y_values[-1]<-self.strana_lesa:
                self.vysledok=f'ÚSPEŠNE STE SA DOSTALI LESA (minuli ste { len(self.x_values)-1} z { self.pocet_krokov} krokov).'
                break
    

         
        

st.set_page_config(page_title="Random walk")

st.markdown("# Random walk")
st.sidebar.header("Random walk")
st.sidebar.write("##### Popis:")
st.sidebar.write("""Táto stránka obsahuje 3 inputy - veľkosť strany lesa
                 - to je ten farebný štvorec ,veľkosť kroku - od koľko
                 do koľko sa môže vykonať , ďalši krok a celkový počet krokov.
                 Na základe tohto inputu sa budú náhodne generovať guličky ,
                 ktoré reprezentujú napr. strateného turistu v lese ,
                 ak bol počet krokov na nájdenie cesty z lesa dostačujúci ,
                 tak sa program preruší a vypíše sa výsledok , zároveň sa objaví
                 animovaní graf , ktorý ukazuje postupnosť krokov.Ak nie ,
                 tak dostanete odpoveď , že ste sa stratili v lese a objaví sa video.""")

col1, col2, col3 = st.columns(3)
with col1:
   strana_lesa=st.number_input('Strana lesa(x2):' , min_value=15,max_value=100,step=5 , value=25)

with col2:
   krok=st.slider('Velkost kroka od-do:' , min_value=1,max_value=10,step=1 , value=[4,8])

with col3:
   pocet_krokov=st.number_input('Pocet krokov:' , min_value=5,max_value=100,step=5 , value=20)

col1, col2, col3 = st.columns(3)
with col1:
   pocet_dier=st.number_input('Pocet dier:' , min_value=3,max_value=15,step=1 , value=7)

with col2:
   polomer=st.slider('Polomer dieryod-do:' , min_value=1,max_value=7,step=1 , value=[2])

with col3:
   carodejnica=st.number_input('Carodejnica:' , min_value=0,max_value=1,step=1 , value=1)

od,do = krok
kroky=range(od,do+1)

rw=Randomwalk(pocet_krokov=pocet_krokov, krok=kroky , strana_lesa=strana_lesa)
rw.fill_walk()

point_numbers=range(len(rw.x_values))

x1, y1 = [-strana_lesa,strana_lesa], [strana_lesa,strana_lesa]
x2,y2 = [-strana_lesa,strana_lesa], [-strana_lesa,-strana_lesa]
x3,y3 = [-strana_lesa,-strana_lesa], [-strana_lesa,strana_lesa]
x4,y4 = [strana_lesa,strana_lesa], [-strana_lesa,strana_lesa]

result_text = st.empty()

if rw.vysledok=='STRATILI STE SA V LESE!!':
    result_text.write(rw.vysledok)
    video_file = open('videos/gif.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes , start_time=0 )
    an = True
    
    
else:
    import time

    fig, ax1 = plt.subplots()

    
        

    ax1.plot(x1, y1,color='green', marker = 'o', markerfacecolor='green' )
    ax1.plot(x2, y2,color='green', marker = 'o', markerfacecolor='green' )
    ax1.plot(x3, y3,color='green', marker = 'o', markerfacecolor='green' )
    ax1.plot(x4, y4,color='green', marker = 'o', markerfacecolor='green' )
    ax1.set(xlim=(-(strana_lesa+15), (strana_lesa+15)), ylim=(-(strana_lesa+15), (strana_lesa+15)))
    
    for _ in range(pocet_dier):
        radius = polomer[-1]  # Adjust the radius range as needed

        # Define the middle area radius where you don't want circles
        middle_radius = 5  # Adjust the middle radius as needed

        x, y = None, None

        # Keep generating random coordinates until they are outside the middle area
        while x is None or y is None or (-middle_radius <= x <= middle_radius and -middle_radius <= y <= middle_radius):
            x = random.uniform(-strana_lesa + radius + 5, strana_lesa - radius - 5)
            y = random.uniform(-strana_lesa + radius + 5, strana_lesa - radius - 5)

        circle = plt.Circle((x, y), radius, color='black')
        ax1.add_patch(circle)

    time.sleep(0.6)
    #line, = ax1.plot(rw.x_values,rw.y_values , marker='o', markerfacecolor="green" )
    the_plot = st.pyplot(fig)

    an = True
    import numpy as np
    
    
    
    def animate(i):
        an =True
        vyska = 7
        sirka = 3
        
        if i == 0 and carodejnica == 1:
        # Create random initial coordinates for the red rectangle
            
            x_rect = np.random.uniform(-strana_lesa + 5, strana_lesa - 5)
            y_rect = np.random.uniform(-strana_lesa + 5, strana_lesa - 5)

            # Create a red rectangle (2x4)
            
            rect = plt.Rectangle((x_rect, y_rect), sirka, vyska, color='red')
            ax1.add_patch(rect)

        x, y = rw.x_values[i:i+2], rw.y_values[i:i+2]
        try:
            # Check if the line crosses any black circle (hole)
            for circle in ax1.patches:
                circle_center = circle.center
                circle_radius = circle.radius
                x0, y0 = circle_center
                if ((x[0] - x0)**2 + (y[0] - y0)**2 <= circle_radius**2 or (x[1] - x0)**2 + (y[1] - y0)**2 <= circle_radius**2):
                    line = ax1.plot(x, y, marker='o', markerfacecolor='orange')
                    ax1.text(x[0] + 0.5, y[0] + 0.05, str(i), fontsize=8, color='black')
                    ax1.text(x[1] + 0.5, y[1] + 0.05, str(i+1), fontsize=8, color='white')
                    i = i + 1
                    an = False  # Set 'an' to False to stop the animation
                    the_plot.pyplot(fig)
                    rw.vysledok = 'Spadli ste do diery'
                    return an
                

        except:
            pass
        
        if carodejnica == 1:
            rect = ax1.patches[-1]  # Get the last added rectangle
            x_rect = np.random.uniform(-strana_lesa + 5, strana_lesa - 5)
            y_rect = np.random.uniform(-strana_lesa + 5, strana_lesa - 5)
            rect.set_xy((x_rect, y_rect))
                
            x0, y0 = rect.get_xy()
        
        if carodejnica == 1:
            try: 
                if ((x[1] <= (x0 +sirka) and x[1] >= x0 and y[1] <= (y0 +vyska) and y[1] >= y0)
                    
                ):  # Check if the orange marker is inside the red rectangle
                    #rect.set_xy((x_rect, y_rect))
                    
                    line = ax1.plot(x, y, marker='o', markerfacecolor='orange')
                    ax1.text(x[0] + 0.5, y[0] + 0.05, str(i), fontsize=8, color='black')
                    #ax1.text(x[1] + 0.5, y[1] + 0.05, str(i+1), fontsize=8, color='white')
                    rw.vysledok = 'Chytila vas carodejnica'
                    result_text.write(rw.vysledok)
                    an = False  # Set 'an' to False to stop the animation
                    #rect = ax1.patches[-1]
                
                    the_plot.pyplot(fig)
                    return an
            except:
                pass
        
        line = ax1.plot(x, y, marker='o', markerfacecolor='orange')
        ax1.text(x[0] + 0.5, y[0] + 0.05, str(i), fontsize=8, color='black')
        
    
        the_plot.pyplot(fig)
        return an

    for i in range(len(point_numbers)):
        if an == False:  # Stop the loop if 'an' is False
            
            result_text.write(rw.vysledok)
            break
        an = animate(i)
        time.sleep(0.6)
        
result_text.write(rw.vysledok)    
    
    
plt.style.use('classic')


if an == True:
    fig, (ax1,ax2) = plt.subplots(1,2 , sharey=True, sharex=True , figsize=(16,9), dpi=100)




    ax1.plot(rw.x_values,rw.y_values , marker='o', markerfacecolor="green" )


    ax1.plot(x1, y1, marker = 'o')
    ax1.plot(x2, y2, marker = 'o')
    ax1.plot(x3, y3, marker = 'o')
    ax1.plot(x4, y4, marker = 'o')
    
    ax1.set(xlim=(-(strana_lesa+15), (strana_lesa+15)), ylim=(-(strana_lesa+15), (strana_lesa+15)))

    ax2.scatter(rw.x_values,rw.y_values,s=50 , c=point_numbers ,cmap=plt.cm.Blues)
    ax2.scatter(rw.x_values[0],rw.y_values[0],s=100 , c='yellow')
    ax2.scatter(rw.x_values[-1],rw.y_values[-1],s=100 , c='red')

    st.pyplot(fig)