import pandas as pd
import numpy as np

def import_data(uploaded_file,lst_fea):

    df = pd.read_csv(uploaded_file)
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
        df[col] = df[col].astype(int)
        df[col] = df[col].astype(str)
        df[col] = df[col].replace('-1', np.nan)
    
    df['RPE'] = df['RPE'].fillna(0)

    return df