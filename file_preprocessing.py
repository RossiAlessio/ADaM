import pandas as pd
import numpy as np
import streamlit as st

def import_data(uploaded_file,lst_fea):

    try:
        df = pd.read_csv(uploaded_file)
    except:
        df = pd.read_excel(uploaded_file)
    for i in lst_fea[2:]:
        lst_val = []
        for ii in df[i]:
            try:
                lst_val.append(float(ii))
            except:
                lst_val.append(np.nan)
        df[i] = lst_val
    
    for col in lst_fea[2:]:
        df[col] = df[col].fillna(-1)
        df[col] = df[col].astype(float)
        df[col] = df[col].replace(-1, np.nan)

    df['time'] = [np.nan if str(x)=='nan' else x for x in df['time']]
    df['TL'] = (df['time']*df['RPE']).fillna(0)

    lst_df_player = []
    for player_ in df['player'].unique():
        df_p = df.query("player == @player_").sort_values('date')
        df_p[['time','RPE','TL']] = df_p[['time','RPE','TL']].shift(1)
        df_p = df_p.rename(columns={'time':'time (d-1)','RPE':'RPE (d-1)','TL':'TL (d-1)'})
        lst_df_player.append(df_p)

    df = pd.concat(lst_df_player)

    return df