import streamlit as st
from Controller import MPsStats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean, median, stdev


def ageGraphs(all_ages, AgesButDictionary, term=""):
    print("a")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(all_ages, bins=10, color='red', edgecolor='black')
    ax.set_title(
        f'Ogólny rozkład wiekowy posłów {term} kadencji sejmu', fontsize=16)
    ax.set_xlabel('Wiek', fontsize=14)
    ax.set_ylabel('Liczba członków', fontsize=14)
    st.pyplot(fig)
    for club in AgesButDictionary:
        if len(AgesButDictionary[club]) > 1:
            avgAge = mean(AgesButDictionary[club])
            st.write(
                f"Dla klubu {club} w {term} kandecji sejmu najstarszy członek miał {max(AgesButDictionary[club])} lat, najmłodszy miał {min(AgesButDictionary[club]) } lat, średnia wieku wynosiła {round(avgAge)} lat, mediana wynosiła {median(AgesButDictionary[club])} lat, odchylenie standardowe wynosiło około {round(stdev(AgesButDictionary[club]))} lat")
    st.header(
        "Wykresy rozkłądu wieku klubów ")
    for club in AgesButDictionary:
        fig, ax = plt.subplots(figsize=(10, 6))
        if len(AgesButDictionary[club]) > 2:
            ax.hist(AgesButDictionary[club], bins=10,
                    color='red', edgecolor='black')
            ax.set_title(
                f'Ogólny rozkład wiekowy klubu {club} dla {term} kadencji sejmu', fontsize=16)
            ax.set_xlabel('Wiek', fontsize=14)
            ax.set_ylabel('Liczba członków', fontsize=14)
            st.pyplot(fig)


def MoreStats(ChosenDictionary):
    st.write(
        "wykresy dla klubów jeśli cczłonkowie mają rózne wykształcenie")
    for club in ChosenDictionary:
        if len(list(ChosenDictionary[club].keys())) > 1:
            fig, ax = plt.subplots(figsize=(10, 5))
            labels = list(ChosenDictionary[club].keys())
            values = list(ChosenDictionary[club].values())
            ax.pie(values, labels=labels)
            ax.set_title(
                f'Wykres dla klubu {club}', fontsize=16)

            st.pyplot(fig)
