import streamlit as st
import pandas as pd
import numpy as np
from file_preprocessing import *
from analysis_plot import *
import datetime

st.set_page_config(layout="wide")

header = st.container()
core = st.container()
sidebar = st.sidebar

lst_fea = ['week','date','RPE','time','TL','fatigue','sleep','sorness','stress','mood']
lst_fea_plot = ['week','date','RPE (d-1)','time (d-1)','TL (d-1)','fatigue','sleep','sorness','stress','mood']


def color_col(val):
    try:
        color = 'lightgreen' if float(val) <= 2 else 'coral' if float(val) >= 4 else 'orange'
    except:
        color = None
    return 'color: %s' % color


with sidebar:
    st.title('ADaM setup')
    st.markdown("---")
    st.write('Add file')

    data_test = st.radio('Vuoi usare il dataset di test?',['SI','NO'],index=0)

    if data_test == 'SI':
        uploaded_file = 'data/data_test.csv'
        st.markdown("---")
        df = import_data(uploaded_file,lst_fea)

    else:
        uploaded_file = st.file_uploader("Choose a CSV or an Excel file",type=['csv','xlsx'])
        st.markdown("---")

        if uploaded_file is not None:

            df = import_data(uploaded_file,lst_fea)

    
    if (uploaded_file is not None) or (data_test == 'SI'):

        df['date'] = [x.date() for x in pd.to_datetime(df['date'])]
        
        st.write('Select analysis options')
        
        lst_date = sorted(df['date'].unique(),reverse=True)
        date_sel = st.selectbox('Select a data to analyse', lst_date)
        date_sel = pd.to_datetime(date_sel).date()

        lst_player = sorted(df['player'].unique(),reverse=False)
        player_sel = st.selectbox('Select a player to analyse', ['Team']+lst_player)


with header:
    st.title('ADaM questionnaire analysis')


with core:

    if (uploaded_file is not None) or (data_test == 'SI'):
        if player_sel == 'Team':
            df_week = df[df['date']<=date_sel][lst_fea_plot].dropna()
            lst_df_w = []
            for col in ['TL (d-1)','fatigue','sleep','sorness','stress','mood']:
                df_w = df_week[['date',col]].rename(columns={col:'value'})
                df_w['value'] = df_w['value'].astype(float)
                if col == 'TL (d-1)':
                    df_w = df_w.replace(0,np.nan).groupby('date').agg(lambda x: np.nanmean(x)).reset_index().fillna(0)
                    df_w['date'] = df_w['date']-datetime.timedelta(days=1)
                    df_w = df_w.set_index('date').reindex(pd.date_range(df_w['date'].min(),date_sel)).fillna(0).reset_index()
                    df_w['date'] = [d.date() for d in df_w['index']]
                else:
                    df_w = df_w.groupby('date').agg(lambda x: np.nanmean(x)).reset_index()
                    #df_w = df_w.set_index('date').reindex(pd.date_range(df_w['date'].min(),date_sel)).fillna(0).reset_index()
                df_w = df_w.sort_values('date')#.set_index('date').rolling(5,min_periods=1).mean().reset_index()
                df_w['group']=col
                lst_df_w.append(df_w)
            df_w_ = pd.concat(lst_df_w)
            date_ = date_sel-datetime.timedelta(days=20)
            df_ = df[df['date']==date_sel]

        else:
            df_week = df[(df['date']<=date_sel)&(df['player']==player_sel)][lst_fea_plot].dropna()
            lst_df_w = []
            for col in ['TL (d-1)','fatigue','sleep','sorness','stress','mood']:
                df_w = df_week[['date',col]].rename(columns={col:'value'})
                df_w['value'] = df_w['value'].astype(float)
                if col == 'TL (d-1)':
                    df_w = df_w.replace(0,np.nan).groupby('date').agg(lambda x: np.nanmean(x)).reset_index().fillna(0)
                    df_w['date'] = df_w['date']-datetime.timedelta(days=1)
                    df_w = df_w.set_index('date').reindex(pd.date_range(df_w['date'].min(),date_sel)).fillna(0).reset_index()
                    df_w['date'] = [d.date() for d in df_w['index']]
                else:
                    df_w = df_w.groupby('date').agg(lambda x: np.nanmean(x)).reset_index()
                    #df_w = df_w.set_index('date').reindex(pd.date_range(df_w['date'].min(),date_sel)).fillna(0).reset_index()
                df_w = df_w.sort_values('date')#.set_index('date').rolling(5,min_periods=1).mean().reset_index()
                df_w['group']=col
                lst_df_w.append(df_w)

            df_w_ = pd.concat(lst_df_w)
            date_ = date_sel-datetime.timedelta(days=20)
            
            df_ = df[(df['date']==date_sel)&(df['player']==player_sel)]
            
        st.markdown("---")
        st.header('Trend analysis',divider='green')

        df_w_['group'] = df_w_['group'].replace('TL (d-1)','TL')

        subplot_fig = plotly_dual_axis(df_w_.query("date >= @date_ & group != 'TL'"),
                            df_w_.query("date >= @date_ & group == 'TL'")[2:-1], 
                            title="", y1="value", y2="value")
        
        st.plotly_chart(subplot_fig, theme="streamlit", use_container_width=True)

        
        st.header('Current status',divider='green')
        col1,col2,col3,col4,col5 = st.columns(5)
        try:
            for fea,column,title in zip(['fatigue','sleep','sorness','stress','mood'],
                                [col1,col2,col3,col4,col5],
                                ['fatigue','sleep','soerness','stress','mood']):
                with column:
                    donut_score(df_,date_sel,fea,title)
        except:
            st.write('No data register for this player!')


        st.write('\n\n')
        if player_sel == 'Team':
            st.table(df[df['date']==date_sel].set_index('player')[lst_fea_plot]\
                            .style.applymap(color_col, subset=['fatigue','sleep','sorness','stress','mood'])\
                                    .format({'RPE (d-1)': "{:.1f}",
                                            'time (d-1)': "{:.0f}",
                                            'TL (d-1)': "{:.0f}",
                                            'fatigue': "{:.0f}",
                                            'sleep': "{:.0f}",
                                            'sorness': "{:.0f}",
                                            'stress': "{:.0f}",
                                            'mood': "{:.0f}"},na_rep='---'))
        else:
            try:
                st.table(df[df['date']==date_sel].set_index('player')[lst_fea_plot]\
                            .style.applymap(color_col, subset=['fatigue','sleep','sorness','stress','mood'])\
                                    .applymap(lambda _: "background-color: darkblue;", subset=([player_sel], slice(None)))\
                                    .format({'RPE (d-1)': "{:.1f}",
                                            'time (d-1)': "{:.0f}",
                                            'TL (d-1)': "{:.0f}",
                                            'fatigue': "{:.0f}",
                                            'sleep': "{:.0f}",
                                            'sorness': "{:.0f}",
                                            'stress': "{:.0f}",
                                            'mood': "{:.0f}"},na_rep='---'))
            except:
                st.table(df[df['date']==date_sel].set_index('player')[lst_fea_plot]\
                            .style.applymap(color_col, subset=['fatigue','sleep','sorness','stress','mood'])\
                                    .format({'RPE (d-1)': "{:.1f}",
                                            'time (d-1)': "{:.0f}",
                                            'TL (d-1)': "{:.0f}",
                                            'fatigue': "{:.0f}",
                                            'sleep': "{:.0f}",
                                            'sorness': "{:.0f}",
                                            'stress': "{:.0f}",
                                            'mood': "{:.0f}"},na_rep='---'))
        
    else:
        st.markdown('Please add a dataset to continue!')
            