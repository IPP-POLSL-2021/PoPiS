import streamlit as st
# from Controller import MPsStats
# import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statistics import mean, median, stdev


def ageGraphs(all_ages, AgesButDictionary, term="", MPsInfoDataFrame="", alldata=True):
    # General age distribution histogram
    fig = px.histogram(
        x=all_ages,
        nbins=10,
        title=f'Ogólny rozkład wiekowy posłów {term} kadencji sejmu',
        labels={'x': 'Wiek', 'y': 'Liczba członków'},
        color_discrete_sequence=['orange']

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
    youngest, oldest = st.columns(2)

    st.dataframe(df, use_container_width=True)
    if alldata == True:
        with oldest:
            # MPsInfoDataFrame = MPsInfoDataFrame.astype(int)

            OldestMP = MPsInfoDataFrame.loc[
                MPsInfoDataFrame.groupby('Club')['Age'].idxmax()]
            st.write(OldestMP)
        with youngest:
            youngestsMP = MPsInfoDataFrame.loc[
                MPsInfoDataFrame.groupby('Club')['Age'].idxmin()]
            st.write(youngestsMP)
        st.header(
            f"Wykresy rozkładu wieku klubów i kół w {term} kadencji sejmu:")
        for club, ages in AgesButDictionary.items():
            if len(ages) > 2:
                fig = px.histogram(
                    x=ages,
                    nbins=10,
                    title=f'{club}',
                    labels={'x': 'Wiek', 'y': 'Liczba członków'},
                    color_discrete_sequence=['purple']
                )
                fig.update_layout(
                    xaxis_title='Wiek',
                    yaxis_title='Liczba członków'
                )
                st.plotly_chart(fig)


def MoreStats(ChosenDictionary):
    st.write("Statystyki dla posłów w poszczególnych klubach:")
    for club, data in ChosenDictionary.items():

        labels = list(data.keys())
        values = list(data.values())
        fig = go.Figure(
            data=[go.Pie(labels=labels, values=values)]
        )
        fig.update_layout(
            title=f'{club}',
        )
        st.plotly_chart(fig)
