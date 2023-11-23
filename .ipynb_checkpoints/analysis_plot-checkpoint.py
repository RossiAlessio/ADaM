import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from math import pi

def donut_score(df,data_sel,fea,title):

    df_ = df[df['date']==data_sel][[fea]]
    df_ = df_.astype(float).mean()
    
    fig, ax = plt.subplots(1,1,figsize=(6,6), subplot_kw={'projection':'polar'})
    value = df_.values[0]
    perc_min = value
    data = perc_min
    data2= 5
    startangle = 90
    x = (data * pi *2)/ 5
    y = (data2 * pi *2)/ 5
    left = (startangle * pi *2)/ 360 #this is to control where the bar starts

    plt.xticks([])
    plt.yticks([])
    ax.spines.clear()

    ax.barh(1, y, left=left, height=1.5, color='k') 
    if data <=2:
        color = 'green'
    elif 2<data<4:
        color = 'orange'
    else:
        color = 'red'
    ax.barh(1, x, left=left, height=1.5, color=color)

    plt.ylim(-3, 3)
    plt.text(0, -3, '%.2f'%value, ha='center', va='center', fontsize=32, c='white')
    plt.title(title.upper(), y=-0.01,fontsize=30, loc='center', c='white')

    # fig.tight_layout()
    st.pyplot(fig,transparent=True)
    # plt.show()