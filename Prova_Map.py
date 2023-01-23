import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
#import plotly.graph_objects as go


#simply plotting a map with no parameters
#st.map()

#creating a sample data consisting different points 
Needed = pd.read_csv(r"Case.csv", sep=";", decimal=",")

#Needed.latitude = pd.to_numeric(Needed.latitude) 
#Needed.longitude = pd.to_numeric(Needed.longitude) 
dataframe = Needed.drop(["latitude","longitude","Riferimento","Prezzo_nome","Color","Indice"],axis=1)

def create_link(url:str) -> str:
    return f'''<a href="{url}">🔗</a>'''

dataframe['Url'] = [create_link(url) for url in dataframe["Url"]]

"# Casa a Milano: Cercasi!"

fig = go.Figure(
    data=[
        go.Table(
            columnwidth = [0.5,0.5,2,0.7,0.7,1],
            header=dict(
                values=[f"<b>{i}</b>" for i in dataframe.columns.to_list()],
                fill_color='Blue',
                font=dict(color='white', size=10)
                ),
            cells=dict(
                values=dataframe.transpose()
                )
            )
        ]
    )
st.plotly_chart(fig, use_container_width=True)

#Needed = dataframe.drop(["latitude","longitude","Riferimento"],axis=1)
#st.write(Needed.to_html(escape=False, index=False), unsafe_allow_html=True)

#plotting a map with the above defined points
#st.map(Needed[["latitude","longitude","Color"]])

gne = Needed[["Indice","latitude","longitude","Prezzo","Color","Riferimento"]]
Locations = Needed[Needed.Riferimento==0]
References = Needed[Needed.Riferimento==1]

tooltip = {
    "html":
        "<b>Prezzo:</b> {Prezzo} <br/>",
        #"<b>Rain:</b> {prec} mm<br/>",
    "style": {
        "backgroundColor": "steelblue",
        "color": "black",
    }
}

view_state = pdk.ViewState(latitude=45.46,longitude=9.18,zoom=10.5)
tooltip = {
    "html":
        "<b>Prezzo:</b> {Prezzo_nome} <br/>"
        "<b>Indice:</b> {Indice} <br/>",
    "style": {
        "backgroundColor": "steelblue",
        "color": "black",
    }
}

slayer = pdk.Layer(
    type='ScatterplotLayer',
    data=Locations,
    get_position=["longitude", "latitude"],
    get_color=[250,0,0,200],
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
    get_color=[120,250,0,200],
    get_line_color=[0, 0, 0],
    get_radius=200,
    pickable=True,
    onClick=True,
    filled=True,
    line_width_min_pixels=10,
    opacity=2,
)

layert1 = pdk.Layer(
    type="TextLayer",
    data=Locations,
    pickable=False,
    get_position=["longitude", "latitude"],
    get_text="Prezzo",
    get_size=3000,
    sizeUnits='meters',
    get_color=[0, 0, 0],
    get_angle=0,
    # Note that string constants in pydeck are explicitly passed as strings
    # This distinguishes them from columns in a data set
    getTextAnchor= '"middle"',
    get_alignment_baseline='"bottom"'
)

pp = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    map_provider='mapbox',
    layers=[
        slayer,
        slayer2,
        layert1,
    ],
    tooltip=tooltip
)

deckchart = st.pydeck_chart(pp)
