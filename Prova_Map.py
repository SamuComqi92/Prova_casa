import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

#Data 
Needed = pd.read_csv(r"Case.csv", sep=";", decimal=",")
Needed.Indice = Needed.Indice.astype(str)
dataframe = Needed.drop(["latitude","longitude","Prezzo_nome","Color"],axis=1)
dataframe = dataframe[dataframe.Riferimento==0]
dataframe = dataframe.drop("Riferimento", axis=1)

#Order by
Order = st.selectbox(
    'Come vuoi ordinare i dati?',
     ("Locali","Metri quadri","Prezzo"))

if Order == "Locali":
    dataframe = dataframe.sort_values(by=['Locali'])
elif Order == "Metri quadri" :
    dataframe = dataframe.sort_values(by=['Metri quadri'])
elif Order == "Prezzo" :
    dataframe = dataframe.sort_values(by=['Prezzo'])
    
def create_link(url:str) -> str:
    return f'''<a href="{url}">🔗</a>'''

dataframe['Url'] = [create_link(url) for url in dataframe["Url"]]

#Title
"# Casa a Milano: Cercasi!"

# link is the column with hyperlinks
dataframe = dataframe.to_html(escape=False, index=False) 
st.write(dataframe, unsafe_allow_html=True)

Locations = Needed[Needed.Riferimento==0]
References = Needed[Needed.Riferimento==1]
view_state = pdk.ViewState(latitude=45.46,longitude=9.18,zoom=10.5)
tooltip = {
    "html":
        "<b>Prezzo:</b> {Prezzo_nome} <br/>"
        "<b>Indice:</b> {Indice} <br/>",
    "style": {
        "backgroundColor": "steelblue",
        "color": "black",
    }}

slayer = pdk.Layer(
    type='ScatterplotLayer',
    data=Locations,
    get_position=["longitude", "latitude"],
    get_color=[250,0,0,500],
    get_line_color=[0, 0, 0],
    get_radius=200,
    pickable=True,
    onClick=True,
    filled=True,
    line_width_min_pixels=10,
    opacity=2,
)

slayer2 = pdk.Layer(
    type='ScatterplotLayer',
    data=References,
    get_position=["longitude", "latitude"],
    get_color=[120,250,0,30],
    get_line_color=[0, 0, 0],
    get_radius=1300,
    pickable=True,
    onClick=True,
    filled=True,
    line_width_min_pixels=10,
    opacity=2,
)

layert1 = pdk.Layer(
    type="TextLayer",
    data=Locations,
    pickable=True,
    get_position=["longitude", "latitude"],
    get_text='Indice',
    billboard=False,
    get_size=13,
    #sizeUnits='meters',
    get_color=[255, 255, 255],
    get_angle=0,
    getTextAnchor= '"middle"',
    get_alignment_baseline='"center"'
)

pp = pdk.Deck(
    #map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    map_provider='mapbox',
    map_style = 'dark', #, ‘dark’, ‘road’, ‘satellite’, ‘dark_no_labels’, and ‘light_no_labels’, a 
    layers=[
        slayer,
        slayer2,
        layert1,
    ],
    tooltip=tooltip
)

deckchart = st.pydeck_chart(pp)
