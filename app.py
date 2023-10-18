import requests as rq
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from streamlit_folium import st_folium
import folium
from folium import IFrame
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import urllib.request
import base64
import os
import streamlit.components.v1 as components
from datetime import date
from io import BytesIO

d_index = 1

  
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Tracking de Diligencias", page_icon=":round_pushpin:", layout="wide",)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# READ EXCEL DATA FROM BLUEMESSAGING
@st.cache_data
def get_data_blue():
    #url = 'https://raw.githubusercontent.com/Dan399/streamlit_tracker_map/Data/DataBluemessaging2023-2023.xlsx'
    url = 'https://raw.githubusercontent.com/Dan399/streamlit_tracker_map/main/Data/DataBluemessaging2023-2023.csv'
    df_blue = pd.read_csv(url, converters={'nrp':str, 'user':str})
    #df_blue['fecha_accion_fiscal'] = pd.to_datetime(df_blue['fecha_accion_fiscal']).dt.date
    print(df_blue.head())
    #print(df_blue['fecha_accion_fiscal'].head())
    return df_blue

df_bluemessaging = get_data_blue()  # Call function to read BIMESTRES_AÑOS

# READ EXCEL DATA FROM NOTIFICADORES LIST
@st.cache_data
def get_data_notif():
    #url2 = 'https://raw.githubusercontent.com/Dan399/streamlit_tracker_map/Data/notif_data.xlsx'
    url2 = 'https://raw.githubusercontent.com/Dan399/streamlit_tracker_map/main/Data/notif_data.csv'
    # data2 = rq.get(url2).content
    # df = pd.read_csv(url,
    #df_notif = pd.read_csv(url2)
    df_notif = pd.read_csv(url2, converters={'usuario_Blue_Naa':str})
    print(df_notif.head())

    return df_notif

df_notificadores = get_data_notif()  # Call function to read database notificadores


def load_initial_map():
    global CircuitsMap
    # Creating the Folium Map 
    CircuitsMap = folium.Map(location=[df_selection["foto_domicilio.lat"].mean(), 
                                    df_selection["foto_domicilio.lng"].mean()], 
                                    zoom_start=12, 
                                    control_scale=True, 
                                    tiles='openstreetmap')
    # Zoom to LAT, LONG bounds
    lft_dwn = df_selection[['foto_domicilio.lat', 'foto_domicilio.lng']].min().values.tolist() # Left Down
    top_rgt = df_selection[['foto_domicilio.lat', 'foto_domicilio.lng']].max().values.tolist() # Top Right
    #print("left:",lft_dwn, "top: ", top_rgt)
    CircuitsMap.fit_bounds([lft_dwn, top_rgt])



def load_marks():
    
    for index, location_info in df_selection.iterrows():
       
        if pd.isna(location_info["foto_domicilio.lat"]) == False and pd.isna(location_info["foto_domicilio.lng"]) == False:
          
            folium.Marker([location_info["foto_domicilio.lat"], location_info["foto_domicilio.lng"]],        
                          #popup = folium.Popup(image),
                          #popup = htmlcode,
                          #tooltip=tooltip).add_to(CircuitsMap)
                          tooltip = 'ID Dataframe: <b>'+ str(index)
                          + '</b><br> Razón Social: <b>'+ str(location_info["razonSocial"]) 
                          + '</b><br> Folio: <b>'+ str(location_info["folio"]) 
                          #+ '</b><br> Lote: <b>'+ str(location_info["lote"]) 
                          + '</b><br> Periodo: <b>'+ str(location_info["periodo"]) 
                          + '</b><br> Domicilio: <b>'+ str(location_info["domicilio"]) 
                          + '</b><br> Municipio: <b>'+ str(location_info["municipio"]) 
                          + '</b><br> Fecha acción: <b>'+ str(location_info["fecha_accion_fiscal"])#).add_to(CircuitsMap)
                          + '</b><br>', 
                          popup = 'ID Dataframe: <b>'+ str(index)
                          + '</b><br> Razón Social: <b>'+ str(location_info["razonSocial"]) 
                          + '</b><br> Folio: <b>'+ str(location_info["folio"]) 
                          + '</b><br> Lote: <b>'+ str(location_info["lote"]) 
                          + '</b><br> Periodo: <b>'+ str(location_info["periodo"]) 
                          + '</b><br> Domicilio: <b>'+ str(location_info["domicilio"]) 
                          + '</b><br> Municipio: <b>'+ str(location_info["municipio"]) 
                          + '</b><br> Fecha acción: <b>'+ str(location_info["fecha_accion_fiscal"])#).add_to(CircuitsMap)
                          + '</b><br>'
                         ).add_to(CircuitsMap)
            


# ----  MAINPAGE ----
st.subheader("🌎 Seguimiento de diligencias de notificación en campo")
st.markdown("""---""")   

# ---- SIDEBAR ----
st.sidebar.subheader(":mag: Buscar Notificador")

id_notif = df_notificadores['usuario_Blue_Naa'].drop_duplicates()
notif = st.sidebar.selectbox('Seleccionar notificador 👥', df_notificadores['nombre_Candidato'])
notifsel = df_notificadores[df_notificadores['nombre_Candidato'] == notif]
notitext = notifsel['usuario_Blue_Naa'].to_string(index=False)
fechas = pd.to_datetime(df_bluemessaging['fecha_accion_fiscal'].unique(), infer_datetime_format=True)

fec_ini = fechas.min()
fec_fin = fechas.max()
#fec_ini = date(2023,1,1)
#fec_fin = date.today()
date1 = st.sidebar.date_input('Fecha inicial 📅', fec_ini)
date2 = st.sidebar.date_input('Fecha final 📅', fec_fin)
#print(df_bluemessaging.head())
#print(notitext)
# print("Date1: ", date1)
# print("Date2: ", date2)
# print("-----------------------")
#[-95.7087615086,10.1905607582],[-118.7181982644,30.3492726304],[-109.0328869405,38.8158651902],[-86.0234501847,20.1199131521],[-95.7087615086,10.1905607582]
#[-92.3283874989,14.5885884023],[-94.5256531239,16.1141217391],[-97.7776062489,15.9451751226],[-101.2053406239,17.1247349144],[-105.6877624989,19.957557521],[-105.4240906239,21.764302789],[-109.1154968739,25.8638772468],[-109.7307312489,26.7306058476],[-112.3674499989,29.5970623379],[-113.5979187489,31.3392882365],[-115.0920593739,31.6390786184],[-114.4768249989,29.5970623379],[-111.8401062489,26.4948690253],[-111.1369812489,25.0703816725],[-109.2912781239,23.3066508335],[-110.2580749989,22.9024472355],[-112.6311218739,26.0219450146],[-114.9162781239,27.3568462745],[-114.4768249989,28.4442612274],[-115.7072937489,30.0545529191],[-117.0256531239,32.4585197615],[-108.4123718739,31.2641907115],[-106.2151062489,31.6390786184],[-103.4904968739,28.9838360496],[-101.8205749989,29.9022888745],[-99.7111999989,27.8242185542],[-99.3596374989,26.416182277],[-97.3381531239,25.8638772468],[-97.6018249989,22.2532152264],[-96.5471374989,19.7095262979],[-94.7014343739,18.3802869579],[-91.8010437489,18.3802869579],[-90.6584656239,19.7922463776],[-90.4826843739,21.0278098541],[-88.3733093739,21.355597764],[-86.8791687489,21.2737190194],[-87.4944031239,19.3782194347],[-88.1096374989,17.7954596447],[-90.0432312489,17.7954596447],[-91.3615906239,17.3765456982],[-90.1311218739,16.1141217391],[-92.2404968739,16.1141217391],[-92.3283874989,14.5885884023]
#[-87.1428406239,21.2737190194],[-117.2893249989,32.310077012]



if notif:
    
    #df_selection = df_bluemessaging[(df_bluemessaging['user'] == notitext) & (df_bluemessaging['fecha_accion_fiscal'] >= date1)  & (df_bluemessaging['fecha_accion_fiscal'] < date2) ]  
    df_selection = df_bluemessaging[(df_bluemessaging['user'] == notitext)]  
    print(df_selection.head())
    df_selection_notif = df_notificadores[df_notificadores['usuario_Blue_Naa'] == notitext]
    num_days = len(df_selection['fecha_accion_fiscal'].unique())
    #print(df_bluemessaging['user'].dtype)
    #print(df_selection.head())
    #print(df_selection_notif.head())
    
    if df_selection.empty:
        st.sidebar.markdown("""---""")
        st.sidebar.caption("### :blue[No existen datos para este Notificador]")
    else:
        st.sidebar.markdown("""---""")
        st.sidebar.caption(f"### **ID Notificador:** :blue[{df_selection_notif['usuario_Blue_Naa'].iloc[-1]}]")
        st.sidebar.caption(f"### **Nombre:** :blue[{df_selection_notif['nombre_Candidato'].iloc[-1]}]")
        st.sidebar.caption(f"### **Despacho:** :blue[{df_selection_notif['despacho'].iloc[-1]}]")
        st.sidebar.caption(f"### **Carta Acreditación NAA:** :blue[{df_selection_notif['folio_Acred_Naa'].iloc[-1]}]")
        st.sidebar.caption(f"### **Carta Acreditación PAE:** :blue[{df_selection_notif['folio_Acred_Pae'].iloc[-1]}]")
        st.sidebar.caption(f"### **RFC:** :blue[{df_selection_notif['rfc'].iloc[-1]}]")
        st.sidebar.caption(f"### **CURP:** :blue[{df_selection_notif['curp'].iloc[-1]}]")
            # CALL FUNCTIONS TO LOAD INITIAL MAP, CHANGE CHECKBOX AND LOAD MARKS
            #initial_query = "nrp == @nrp"
    
        load_initial_map()
        load_marks()
            #load_images()
            #change_checkbox()
        #st_Data = st_folium(CircuitsMap, width=1000, height=600)
        
        fig_notif_diaria = px.histogram(
            df_selection,
            x="nombre_estatus",
            y="folio",
            histfunc='count',
            text_auto= True,
            title="<b>Diligencias por estatus del notificador seleccionado</b>",
            template="plotly_white",
            labels={"nombre_estatus": "Estatus", "folio": "Numero de Folios"},
            #color_discrete_sequence= ["#E31937"],
        )
        fig_notif_diaria.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            #xaxis_tickprefix = '$', 
            yaxis_tickformat = ',.0f',
            showlegend = True,
            bargap = 0.1)
        
        left_column, right_column = st.columns([3,2])
        #left_column.st_folium(CircuitsMap) width=1000, height=600
        with left_column:
            st_Data = st_folium(CircuitsMap, width=750, height=550)

        right_column.plotly_chart(fig_notif_diaria, use_container_width=True)

        st.markdown("""---""")
        #df_style = df_selection.style.apply()
        #st.dataframe(df_selection.style.apply(color_coding(d_index), axis=1))
        #st.dataframe(df_selection.style.map_index(color_coding))
        #st.dataframe(df_selection.style.apply(color_coding, axis=1))
        st.dataframe(df_selection)
else:
    st.sidebar.markdown("""---""")
    st.sidebar.caption("### :blue[Seleccione un Notificador]")    








