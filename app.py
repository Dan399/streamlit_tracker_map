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
import requests as rq
from io import BytesIO

d_index = 1

  
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Tracking de Diligencias Exitosas", page_icon=":round_pushpin:", layout="wide",)



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
  
    url = 'https://raw.githubusercontent.com/Dan399/streamlit_tracker_map/Data/DataBluemessaging2023-2023.xlsx'
    data = rq.get(url).content
    #df = pd.read_excel(BytesIO(data))
    df_blue = pd.read_excel(BytesIO(data), converters={'nrp':str, 'user':str, 'foto_domicilio.lat':float, 'foto_domicilio.lng':float}, engine='openpyxl')
    df_blue['fecha_accion_fiscal'] = pd.to_datetime(df_blue['fecha_accion_fiscal']).dt.date
    #print(df_blue['fecha_accion_fiscal'].head())
    return df_blue

df_bluemessaging = get_data_blue()  # Call function to read BIMESTRES_AÑOS

# READ EXCEL DATA FROM NOTIFICADORES LIST
@st.cache_data
def get_data_notif():
    url2 = 'https://raw.githubusercontent.com/Dan399/streamlit_tracker_map/Data/notif_data.xlsx'
    data2 = rq.get(url2).content
    df_notif = pd.read_excel(BytesIO(data2), 
    converters={'usuario_Blue_Naa':str}, engine='openpyxl')
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


# def change_checkbox():
#     val = [None]* len(estatus) # this list will store info about which category is selected
#     #query_str = ""
#     query_str2 = []
#     st.sidebar.markdown("""---""")
#     st.sidebar.subheader("Selecciona el estatus a Mapear")
#     for i, cat in enumerate(estatus):
#         # create a checkbox for each category
#         if cat == 'Notificado 1a. Visita' or cat == 'Notificado 2a. Visita':
#             val[i] = st.sidebar.checkbox(cat, value=True) #, on_change=load_marks) # value is the preselect value for first render
#         else:
#             val[i] = st.sidebar.checkbox(cat, value=False) #, on_change=load_marks) # value is the preselect value for first render
#         if val[i] == True:
#             #query_str = query_str + " & nombre_estatus == '"+ cat +"'"
#             query_str2.append(cat)
#     #multiselect = st.sidebar.multiselect("Selecciona los estatus que deseas mapear", query_str2)    
#     #print(val[i],cat)
#     #query_str = '"nrp == @nrp' + query_str + '"'    
#     #print(query_str2)
#     #print("Call Load Images")
#     #load_images()
#     load_marks(query_str2)    

#def select_checkbox():
def load_marks():
    #df_selection2 = df_selection[df_selection["nombre_estatus"].isin(multiselect)]
    #df_selection2["image"] = load_images(df_selection2)
    #df_selection = df_bluemessaging.query(query_str)
    #df_selection = df_bluemessaging.query("nrp == @nrp & nombre_estatus == 'Notificado 2a. Visita'")
    #df_selection = df_bluemessaging[~df_bluemessaging['nombre_estatus'].isin(query_str2)]
    #df_selection = df_bluemessaging[df_bluemessaging['nrp'] == "@nrp"]
    #print(df_selection.head(6))
    #popup = load_images(df_selection2)
    #print("Load Marks")
    
    for index, location_info in df_selection.iterrows():
       
        if pd.isna(location_info["foto_domicilio.lat"]) == False and pd.isna(location_info["foto_domicilio.lng"]) == False:
            #location_info["image"] = load_images(location_info["foto_domicilio.src"])
            #print(str(location_info["image"]))
            #print(str(df_selection2.at[index,'imagen']))
            #imagen = Image.open(location_info["image"])
            #image = folium.IFrame("<img src='" + str(location_info["image"]) + "'>")
            #image = folium.IFrame(imagen)
            #imagen = "<img src='" + str(location_info["image"]) + "' width=300>" 
            # html = '<figure>'
            # encoded = base64.b64encode(open(str(df_selection2.at[index,'imagen']), 'rb').read()).decode()
            # html += '<img src="data:image/jpeg;base64,{}">'.format(encoded)
            # html += '</figure>'
            # #html = '<img src="data:image/jpeg;base64,{}">'.format
            # #encoded = base64.b64encode(open(str(df_selection2.at[index,'imagen']), 'rb').read()).decode()
            # iframe = folium.IFrame(html, width = 300, height=300)
            # tooltip = folium.Tooltip(iframe)
            #icon=folium.IFrame('<i class="fas fa-archway"></i>')
            #print(str(df_selection2.at[index,'imagen']))
            #imagen_ = '<img src="' + str(df_selection2.at[index,'imagen']) + '" width=300>'
            #htmlcode = """<div><img src="C:\Users\IN334906\Lenovo Old\2022\45_PYTHON PROJECTS\Streamlit\1_YTB_Proy1\Streamlit-MapNotificadores\b1inbuginq2a.jpg" alt="Flowers in Chania" width="230" height="172"><br /><span>Flowers in Chania</span></div>"""
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
            

#def load_images():
    #print("Load Images")    
    #i=0
        #imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
    #for index, location_info in df_selection.iterrows():
    #    i=i+1
    #    src_ini = location_info["foto_domicilio.src"]
    #    src_end = src_ini.replace('.xsp','')
    #    src_end_img = str(src_end[-12:]) + ".jpg"
    #    urllib.request.urlretrieve(src_end, src_end_img)
        #img = Image.open(src_end_img)
    #    imageUrls = os.path.abspath(src_end_img)
        
    #    df_selection.at[index,'imagen'] = str(imageUrls)
        
        #print(location_info["imagen"])
        #selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)

        # if imageUrls:
        #     st.image(imageUrls)
        #encoded = base64.b64encode(open(src_end_img, 'rb').read())
        #html = '<img src="data:image/jpg;base64,{}">'.format
        #print(df_selection.at[index,'imagen'])
    
        #print(df_selection[index,"imagen"])
    #print("Iteraciones: {}", i)
    #return df_selection

# ----  MAINPAGE ----
st.subheader("🌎 Seguimiento a despachos de notificación - Infonavit Delegación Quintana Roo")
st.markdown("""---""")   

# ---- SIDEBAR ----
st.sidebar.subheader(":mag: Buscar Notificador")

id_notif = df_notificadores['usuario_Blue_Naa'].drop_duplicates()
notif = st.sidebar.selectbox('Seleccionar notificador 👥', df_notificadores['nombre_Candidato'])
notifsel = df_notificadores[df_notificadores['nombre_Candidato'] == notif]
notitext = notifsel['usuario_Blue_Naa'].to_string(index=False)
#print(df_bluemessaging['fecha_accion_fiscal'].dtype)
fechas = pd.to_datetime(df_bluemessaging['fecha_accion_fiscal'].unique())
fec_ini = fechas.min(skipna = True)
fec_fin = fechas.max(skipna = True)
#fec_ini = date(2023,1,1)
#fec_fin = date.today()
date1 = st.sidebar.date_input('Fecha inicial 📅', fec_ini)
date2 = st.sidebar.date_input('Fecha final 📅', fec_fin)
#print(df_bluemessaging.head())
#print(notitext)
# print("Date1: ", date1)
# print("Date2: ", date2)
# print("-----------------------")




if notif:
    
    #df_selection = df_bluemessaging[(df_bluemessaging['user'] == notitext) & (df_bluemessaging['fecha_accion_fiscal'] >= date1)  & (df_bluemessaging['fecha_accion_fiscal'] < date2) ]  
    df_selection = df_bluemessaging[(df_bluemessaging['user'] == notitext)]  
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
            st_Data = st_folium(CircuitsMap, width=1000, height=600)

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




