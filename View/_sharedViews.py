import streamlit as st
from Controller import MPsStats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid
from statistics import mean, median, stdev

def ageGraphs(all_ages, AgesButDictionary, term=""):
    # General age distribution histogram
    fig = px.histogram(
        x=all_ages, 
        nbins=10, 
        title=f'Ogólny rozkład wiekowy posłów {term} kadencji sejmu',
        labels={'x': 'Wiek', 'y': 'Liczba członków'},
        color_discrete_sequence=['red']
    )
    fig.update_layout(
        xaxis_title='Wiek',
        yaxis_title='Liczba członków'
    )
    st.plotly_chart(fig)

    data = []
    for club, ages in AgesButDictionary.items():
        if len(ages) > 1:
            avg_age = mean(ages)
            max_age = max(ages)
            min_age = min(ages)
            median_age = median(ages)
            std_dev_age = stdev(ages)
            
            data.append({
                'Klub': club,
                'Najstarszy członek (lat)': max_age,
                'Najmłodszy członek (lat)': min_age,
                'Średnia wieku (lat)': round(avg_age),
                'Mediana wieku (lat)': median_age,
                'Odchylenie standardowe (lat)': round(std_dev_age)
            })

    # Create and display the DataFrame inline
    df = pd.DataFrame(data)
    st.write(f"Statystyki wieku dla klubów w {term} kadencji sejmu:")
    st.dataframe(df, use_container_width=True)

    st.header("Wykresy rozkładu wieku klubów")
    for club, ages in AgesButDictionary.items():
        if len(ages) > 2:
            fig = px.histogram(
                x=ages, 
                nbins=10, 
                title=f'Ogólny rozkład wiekowy klubu {club} dla {term} kadencji sejmu',
                labels={'x': 'Wiek', 'y': 'Liczba członków'},
                color_discrete_sequence=['red']
            )
            fig.update_layout(
                xaxis_title='Wiek',
                yaxis_title='Liczba członków'
            )
            st.plotly_chart(fig)

def MoreStats(ChosenDictionary):
    st.write("Wykresy dla klubów jeśli członkowie mają różne atrybuty")
    for club, data in ChosenDictionary.items():
        if len(data) > 1:
            labels = list(data.keys())
            values = list(data.values())
            fig = go.Figure(
                data=[go.Pie(labels=labels, values=values)]
            )
            fig.update_layout(
                title=f'Wykres dla klubu {club}',
            )
            st.plotly_chart(fig)
