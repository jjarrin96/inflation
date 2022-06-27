# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:19:14 2022

@author: juanj
"""

import altair as alt
import pandas as pd
import streamlit as st
#import altair_viewer
import plotly.express as px


#%% helper functions
def fecha_str(date):
    dict_m = {'ene':'enero', 'feb':'febrero', 'mar':'marzo', 'abr':'abril', 'may':'mayo',
              'jun':'junio', 'jul':'julio', 'ago':'agosto', 'sep':'septiembre',
              'oct':'octubre', 'nov':'noviembre', 'dic':'diciembre'}
    
    y = date[-2:]
    m = date[:3]
    return dict_m[m]+' '+'20'+y

#%%
# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="centered", page_title="Monitor de inflacion", page_icon="📈")

# texto

st.header("Monitor de Inflación")

"""
**Monitor de Inflación**
En esta página puedes monitorear la variación anual y mensual de los precios de los **359 productos que componen la canasta del Índice de Precios al Consumidor (IPC)**. La información ha sido obtenida del Instituto Nacional de Estadística y Censos.
"""


# datos

df_anual = pd.read_csv("https://raw.githubusercontent.com/EnexFG/inflation_tracker/main/InflacionAnual.csv")
df_anual = df_anual.set_index('mes')

df_mensual = pd.read_csv("https://raw.githubusercontent.com/EnexFG/inflation_tracker/main/InflacionMensual.csv")
df_mensual = df_mensual.set_index('mes')

df_cum = pd.read_csv("https://raw.githubusercontent.com/EnexFG/inflation_tracker/main/InflacionAcumulada.csv")
df_cum = df_cum.set_index('mes')

#%%

m_actual = fecha_str(df_mensual.index[-1])

st.header("**Inflación por producto al mes de "+m_actual+"**")

lista_productos = tuple(df_anual.columns.to_list())

option = st.selectbox('Selecciona la cesta de productos:', lista_productos)

ia = df_anual.loc[df_anual.index[-1], option]
im = df_mensual.loc[df_mensual.index[-1], option]
ic = df_cum.loc[df_cum.index[-1], option]

col1, col2, col3 = st.columns(3)
col1.metric("Inflacion anual", str(ia)+"%")
col2.metric("Inflacion mensual", str(im)+"%")
col3.metric("Inflacion acumulada", str(ic)+"%")

df_anual = df_anual.reset_index()

#%%

# Variacion anual

char_var_anual = (alt.Chart(df_anual).
                  mark_line().
                  encode(x= alt.X("mes",title="date"),
                         y = option,
                         tooltip=["mes", alt.Tooltip(option, title="Variación anual")]).
                         configure_axis(grid=False, domain=False))





st.altair_chart(char_var_anual, use_container_width=True)

s_ta = ""
if df_anual.loc[df_anual.index[-1],option]>0:
    s_ta = "+"

st.markdown("La variación de precios **anual** de "+option+" en "+m_actual+" fue "+"**"+s_ta+str(df_anual.loc[df_anual.index[-1],option])+"%**")

# Variacion mensual
fig2 = px.line(df_mensual, y=option, title=u'Inflación mensual de '+option)
fig2.add_hline(y=0.0, line_width=1, line_dash="dash", line_color="red")

fig2.update_yaxes(title=None)
fig2.update_xaxes(title=None)

# range slider
fig2.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True)
    ))

st.plotly_chart(fig2, use_container_width=True)

s_tm = ""
if df_mensual.loc[df_mensual.index[-1],option]>0:
    s_tm = "+"
    
st.markdown("La variación de precios **mensual** de "+option+" en "+m_actual+" fue "+"**"+s_tm+str(df_mensual.loc[df_mensual.index[-1],option])+"%**")


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
