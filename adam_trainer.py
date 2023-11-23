# import libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import datetime
import numpy as np

# set config page
st.set_page_config(page_title='Wellness analysis',layout="wide")

header = st.container()
core = st.container()
sidebar = st.sidebar

# import dataset
df_giocatori = pd.read_csv('data/giocatori.csv')
df_allenamenti = pd.read_csv('data/allenamenti.csv')#.rename(columns={'Data':'date_reg'})

df_wellness = pd.read_csv('data/wellness.csv')
dct_fatigue = {'nessuna fatica':1, 'leggeremente affaticato':2, 'affaticato':3, 'stanco':4, 'molto stanco':5}
dct_soreness = {'nessuno':1, 'leggero':2, 'moderato':3, 'indolenzito':4, 'molto indolenzito':5}
dct_sleep = {'ottima':1, 'discreta':2, 'normale':3, 'scarsa':4, 'pessima':5}
dct_mood = {'molto positivo':1, 'positivo':2, 'neutro':3, 'negativo':4, 'molto negativo':5}
dct_stress = {'molto rilassato':1, 'rilassato':2, 'neutro':3, 'stressato':4, 'molto stressato':5}
for col,dct_ren in zip(['fatica','soreness','sleep','stress','mood'],[dct_fatigue,dct_soreness,dct_sleep,dct_stress,dct_mood]):
    df_wellness[col] = [dct_ren[x] for x in df_wellness[col]]

df_rpe = pd.read_csv('data/rpe.csv')

df_inf = pd.read_csv('data/infortuni.csv')

# set header
with header:
    st.title('Analisi wellness status')

# set page menu navigator
with sidebar:
    selected = option_menu("Main Menu", ["Analisi", 'Giocatori', 'Allenamenti', 'Infortuni'], #aggiungi infortuni e configuratore
        icons=['house', 'gear', 'gear', 'gear'], menu_icon="cast", default_index=0)
    selected

# pages
with core:

    # pagina di analisi
    if selected == 'Analisi':
        date_ = st.selectbox("Data",sorted(df_allenamenti['date_reg'].unique(),reverse=True))

        # mean team per day
        df_wi_team = df_wellness.groupby('date_reg')[['fatica','soreness','sleep','stress','mood']].mean()
        df_rpe_team = df_rpe.groupby('date_reg')[['rpe','durata','TL']].mean()
        #_df_ = df_allenamenti.merge(df_wi,on='date_reg',how='outer').merge(df_rpe,on='date_reg',how='outer').fillna(0)
        _df_team = (round(df_wi_team.merge(df_rpe_team,on='date_reg',how='outer').fillna(0),1)).reset_index()
        _df_team['Nome'] = 'Team'
        
        
        # mean per player
        df_wi_ = df_wellness.groupby(['date_reg','Nome'])[['fatica','soreness','sleep','stress','mood']].mean()
        df_rpe_ = df_rpe.groupby(['date_reg','Nome'])[['rpe','durata','TL']].mean()
        #_df_ = df_allenamenti.merge(df_wi,on='date_reg',how='outer').merge(df_rpe,on='date_reg',how='outer').fillna(0)
        _df_ = df_wi_.merge(df_rpe_,on=['date_reg','Nome'],how='outer').fillna(0).reset_index()
        
        _df_all = pd.concat([_df_,_df_team])
        st.write('')
        st.dataframe(_df_all.query('date_reg == @date_')[['Nome','fatica','soreness','sleep','stress','mood','rpe','durata','TL']],
                        hide_index=True,
                        use_container_width=True)
        

        str_name = st.selectbox("Giocatore",['Team']+list(df_giocatori['Nome'].unique()))
        

        # if str_name == 'Team':
        #    pass 
            
        # else:
        #    pass
        
        


    # pagina giocatori
    elif selected == 'Giocatori':
        
        st.header('Giocatori nel database')
        
        st.dataframe(df_giocatori.sort_values('date_reg').drop_duplicates(subset=['Nome'],keep='last')[['Nome','Data nascita','Peso','Altezza']], 
                     hide_index=True,
                     use_container_width=True)

        with sidebar:
            with st.form("my_form_play",clear_on_submit=True):
                st.write("Aggiungi nuovo giocatore")
                str_name = st.text_input("Nome e congnome")
                date_val = st.date_input("Data di nascita",min_value=pd.to_datetime('1980/01/01').date())
                peso = st.number_input('Peso (kg)',min_value=0)
                altezza = st.number_input('Altezza (cm)',min_value=0)


                submitted = st.form_submit_button("Submit") # Every form must have a submit button.
                if submitted:
                    data_reg = datetime.date.today()
                    df_new = pd.DataFrame([[data_reg,str_name,date_val,peso,altezza]],
                                          columns=['date_reg','Nome','Data nascita','Peso','Altezza'],index=[0])
                    df_giocatori = pd.concat([df_giocatori,df_new]).reset_index(drop=True)
                    for col in list(df_giocatori):
                        if 'Unnam' in col:
                            del df_giocatori[col]
                    df_giocatori.to_csv('data/giocatori.csv')

                    st.rerun()


            with st.form("my_form_play_agg",clear_on_submit=True):
                st.write("Aggiorna dati giocatori")
                str_name = st.selectbox("Nome e congnome",['']+list(df_giocatori['Nome'].unique()))
                date_val = st.date_input("Data di nascita",min_value=pd.to_datetime('1980/01/01').date())
                peso = st.number_input('Peso (kg)',min_value=0)
                altezza = st.number_input('Altezza (cm)',min_value=0)


                submitted = st.form_submit_button("Submit") # Every form must have a submit button.
                if submitted:
                    data_reg = datetime.date.today()
                    df_new = pd.DataFrame([[data_reg,str_name,date_val,peso,altezza]],
                                          columns=['date_reg','Nome','Data nascita','Peso','Altezza'],index=[0])
                    df_giocatori = pd.concat([df_giocatori,df_new]).reset_index(drop=True)
                    for col in list(df_giocatori):
                        if 'Unnam' in col:
                            del df_giocatori[col]
                    df_giocatori.to_csv('data/giocatori.csv')

                    st.rerun()


    # pagina allenamenti
    elif selected == 'Allenamenti':
        
        st.header('Allenamenti creati')

        st.dataframe(df_allenamenti[['date_reg','Tipo','GD','Giocatori']], 
                     hide_index=True,
                     use_container_width=True)

        with sidebar:
            with st.form("my_form_sess",clear_on_submit=True):
                st.write("Aggiungi nuova sessione")
                date_val = st.date_input("Data sessione")
                str_type = st.radio("Tipo di sessione",['Allenamento','Partita','Reconditioning','Individuale'])
                str_gdp = st.number_input("Giorni dalla partita passata",min_value=0,
                                            help='Inserire numero di giorni dalla partita passata.')
                str_gdm = st.number_input("Giorni dalla partita successiva",min_value=0,
                                            help='Inserire numero di giorni mancanti alla partita passata.')
                lst_players = st.multiselect("Seleziona i giocatori",list(df_giocatori['Nome'].unique()))


                submitted = st.form_submit_button("Submit") # Every form must have a submit button.
                if submitted:
                    if str_type != 'Partita':
                        GD = 'GD+%s-%s'%(str_gdp,str_gdm)
                    else:
                        GD = 'GD'

                    df_new_all = pd.DataFrame([[date_val,str_type,GD,lst_players]],
                                              columns=['Data','Tipo','GD','Giocatori'],index=[0])
                    df_allenamenti = pd.concat([df_allenamenti,df_new_all]).reset_index(drop=True)
                    for col in list(df_allenamenti):
                        if 'Unnam' in col:
                            del df_allenamenti[col]

                    df_allenamenti.to_csv('data/allenamenti.csv')

                    st.rerun()


    # pagina inforuni
    elif selected == 'Infortuni':
        
        st.header('Infotuni registrati')

        st.dataframe(df_inf[['Giocatore','Data infortunio','Data fine infortunio','Tipo','note']], 
                     hide_index=True,
                     use_container_width=True)

        with sidebar: # trova modo di far aggiornare data di fine
            with st.form("my_form_inf",clear_on_submit=True):
                st.write("Aggiungi nuovo infortunio")
                str_name = st.selectbox("Nome e congnome",['']+list(df_giocatori['Nome'].unique()))
                date_val = st.date_input("Data infortunio")
                date_end_val = np.nan
                str_type = st.radio("Tipo di infortunio",['Muscolare','Distorsivo','Da contatto','Malattia'])
                str_note = st.text_input('Note')

                submitted = st.form_submit_button("Submit") # Every form must have a submit button.
                if submitted:

                    df_new_all = pd.DataFrame([[str_name,date_val,date_end_val,str_type,str_note]],
                                              columns=['Giocatore','Data infortunio','Data fine infortunio','Tipo','note'],index=[0])
                    df_inf = pd.concat([df_inf,df_new_all]).reset_index(drop=True)
                    for col in list(df_inf):
                        if 'Unnam' in col:
                            del df_inf[col]

                    df_inf.to_csv('data/infortuni.csv')

                    st.rerun()






