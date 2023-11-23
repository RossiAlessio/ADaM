import streamlit as st
import pandas as pd
import numpy as np
from file_preprocessing import *
from analysis_plot import *
import plotly.express as px

st.set_page_config(layout="wide")

header = st.container()
core = st.container()
sidebar = st.sidebar

lst_fea = ['week','date','RPE','time','TL','fatigue','sleep','sorness','stress','mood']

with sidebar:
    st.title('ADaM setup')
    st.markdown("---")
    st.write('Add file')
    
    uploaded_file = st.file_uploader("Choose a CSV or an Excel file",type=['csv','xlsx'])
    st.markdown("---")
    if uploaded_file is not None:

        df = import_data(uploaded_file,lst_fea)
        
        st.write('Select analysis options')
        
        lst_date = sorted(df['date'].unique(),reverse=True)
        date_sel = st.selectbox('Select a data to analyse', lst_date)

        lst_player = sorted(df['player'].unique(),reverse=False)
        player_sel = st.selectbox('Select a player to analyse', ['Team']+lst_player)


with header:
    st.title('ADaM questionnaire analysis')

with core:
    if uploaded_file is not None:

        if player_sel == 'Team':
            df_week = df[df['date']<=date_sel][lst_fea].dropna()[-7:]
            lst_df_w = []
            for col in ['fatigue','sleep','sorness','stress','mood']:
                df_w = df_week[['date',col]].rename(columns={col:'value'})
                df_w['group']=col
                lst_df_w.append(df_w)
            df_w_ = pd.concat(lst_df_w)
            fig = px.bar(df_w_, x="date", y='value', title='Player trend', color="group")
            df_ = df[df['date']==date_sel]
        else:
            df_week = df[(df['date']<=date_sel)&df['player']==player_sel][lst_fea].dropna()[-7:]
            lst_df_w = []
            for col in ['fatigue','sleep','sorness','stress','mood']:
                df_w = df_week[['date',col]].rename(columns={col:'value'})
                df_w['group']=col
                lst_df_w.append(df_w)
            df_w_ = pd.concat(lst_df_w)
            fig = px.bar(df_w_, x="date", y='value', title='Player trend', color="group")
            df_ = df[(df['date']==date_sel)&(df['player']==player_sel)]
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        col1,col2,col3,col4,col5 = st.columns(5)
        for fea,column,title in zip(['fatigue','sleep','sorness','stress','mood'],
                              [col1,col2,col3,col4,col5],
                              ['fatigue','sleep','soerness','stress','mood']):
            with column:
                donut_score(df_,date_sel,fea,title)

        

        st.write()
        st.table(df_[df_['date']==date_sel].set_index('player')[lst_fea])
        