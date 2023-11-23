# import libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime

# set config page
st.set_page_config(page_title='Wellness analysis per giocatore',layout="wide")

header = st.container()
core = st.container()
sidebar = st.sidebar

# import dataset
df_giocatori = pd.read_csv('data/giocatori.csv')
df_wellness = pd.read_csv('data/wellness.csv')

df_rpe = pd.read_csv('data/rpe.csv')
df_allenamenti = pd.read_csv('data/allenamenti.csv').rename(columns={'Data':'date_reg'})

# set header
with header:
    st.title('Analisi wellness status')

# set page menu navigator
with sidebar:
    selected = option_menu("Main Menu", ["Analisi", 'Wellness', 'RPE'], 
        icons=['house', 'gear', 'gear'], menu_icon="cast", default_index=0)
    selected

# pages
with core:

    # pagina di analisi
    if selected == 'Analisi':
        date_ = st.selectbox("Data",sorted(df_allenamenti['date_reg'].unique(),reverse=True))


    # pagina giocatori
    elif selected == 'Wellness':
        
        with st.form("my_form_WI",clear_on_submit=True):
            st.write("Compila questionario Wellness")
            str_name = st.selectbox("Nome e congnome",['']+list(df_giocatori['Nome'].unique()))
            fatigue = st.select_slider('Fatica',options=['nessuna fatica', 'leggeremente affaticato', 'affaticato', 'stanco', 'molto stanco'])
            soreness = st.select_slider('Dolore muscolare',options=['nessuno', 'leggero', 'moderato', 'indolenzito', 'molto indolenzito'])
            sleep = st.select_slider('Qualità del sonno',options=['ottima', 'discreta', 'normale', 'scarsa', 'pessima'])
            mood = st.select_slider('Umore',options=['molto positivo', 'positivo', 'neutro', 'negativo', 'molto negativo'])
            stress = st.select_slider('Stress',options=['molto rilassato', 'rilassato', 'neutro', 'stressato', 'molto stressato'])


            submitted = st.form_submit_button("Submit") # Every form must have a submit button.
            if submitted:
                data_reg = datetime.date.today()
                df_new = pd.DataFrame([[data_reg,str_name,fatigue,soreness,sleep,stress,mood]],
                                          columns=['date_reg','Nome','fatica','soreness','sleep','stress','mood'],index=[0])
                df_wellness = pd.concat([df_wellness,df_new]).reset_index(drop=True)
                for col in list(df_wellness):
                    if 'Unnam' in col:
                        del df_wellness[col]
                df_wellness.to_csv('data/wellness.csv')

                st.rerun()

    elif selected == 'RPE':
        with st.form("my_form_RPE",clear_on_submit=True):
            st.write("Compila questionario RPE")
            str_name = st.selectbox("Nome e congnome",['']+list(df_giocatori['Nome'].unique()))
            rpe = st.slider('RPE',0,10,1)
            dur_val = st.number_input("Durata allenamento in minuti",min_value=0,
                                            help="Inserire la durata dell'allenamento in minuti.")
            TL = dur_val*rpe

            submitted = st.form_submit_button("Submit") # Every form must have a submit button.
            if submitted:
                data_reg = datetime.date.today()
                df_new = pd.DataFrame([[data_reg,str_name,rpe,dur_val,TL]],
                                          columns=['date_reg','Nome','rpe','durata','TL'],index=[0])
                df_rpe = pd.concat([df_rpe,df_new]).reset_index(drop=True)
                for col in list(df_rpe):
                    if 'Unnam' in col:
                        del df_rpe[col]
                df_rpe.to_csv('data/rpe.csv')

                st.rerun()