# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 13:19:14 2022

@author: juanj
"""

import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime as dt
import panel as pn
from altair import datum

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



#%%


# Variacion anual
periods = (2022-2016)*12 + 5
rng = pd.date_range('1/1/2016', periods=periods, freq='M')

highlight = alt.selection(
    type='single', on='mouseover', fields=['mes'], nearest=True)
df_anual = df_anual.iloc[:periods]
df_anual = df_anual.set_index(rng)
df_anual = df_anual.reset_index()



data_start = df_anual["index"].min()
data_end = df_anual["index"].max()

d_s_d = data_start.to_pydatetime()
d_s_e = data_end.to_pydatetime()

s_year = d_s_d.year
s_day = d_s_d.day
s_month = d_s_d.month

e_year = d_s_e.year
e_day = d_s_e.day
e_month = d_s_e.month



df_anual = df_anual.iloc[:periods]
df_anual = df_anual.set_index(rng)
df_anual = df_anual.reset_index()


anual_base = (alt.Chart(df_anual).
              encode(x= alt.X('index:T',
                              axis = alt.Axis(title = 'Date'.upper(), 
                                              format = ("%b %Y"))),
                     y = option))

char_var_anual = anual_base.mark_circle().encode(opacity=alt.value(0),
                                                 tooltip=["mes", alt.Tooltip(option, title="Variación anual")])

lines = anual_base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(5), alt.value(10)))

graph= ((char_var_anual + lines).
        configure_axis(grid=False, domain=False).
        properties(title=u'Inflación mensual de '+option).
        configure_title(anchor='start').
        add_selection(highlight).interactive())

# A slider filter
year_slider = alt.binding_range(data_start, data_end, step=1)
slider_selection = alt.selection_single(bind=year_slider, fields=['index'], name="")


filter_year = (graph.add_selection(slider_selection).
               transform_filter(slider_selection).
               properties(title="Slider Filtering"))



st.altair_chart(graph, use_container_width=True)

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
