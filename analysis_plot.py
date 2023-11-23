import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from math import pi
from plotly.subplots import make_subplots
import plotly.express as px

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


def plotly_dual_axis(data1,data2, title="", y1="", y2=""):
    # Create subplot with secondary axis
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])

    #Put Dataframe in fig1 and fig2
    fig1 = px.line(data1, x="date", y='value',
                          color="group", markers=True)
    fig2 = px.line(data2, x="date", y='value',
                          color="group", markers=True)
    fig2.update_traces(line=dict(color="darkred", width=8))

    #Change the axis for fig2
    fig2.update_traces(yaxis="y2")

    #Add the figs to the subplot figure
    subplot_fig.add_traces(fig1.data + fig2.data)

    #FORMAT subplot figure
    subplot_fig.update_layout(title=title, yaxis=dict(title=y1), yaxis2=dict(title=y2))

    #RECOLOR so as not to have overlapping colors
    subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    #subplot_fig.update_layout(yaxis1_tickvals = [0, 5, 1], yaxis2_tickvals = [0, 1000, 100])

    return subplot_fig