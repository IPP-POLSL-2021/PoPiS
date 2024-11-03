import streamlit as st
from Controller import MPsStats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean, median, stdev
from View import _sharedViews


# def ageGraphs(all_ages, AgesButDictionary, term=""):
#     print("a")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.hist(all_ages, bins=10, color='red', edgecolor='black')
#     ax.set_title(
#         f'Ogólny rozkład wiekowy posłów {term} kadencji sejmu', fontsize=16)
#     ax.set_xlabel('Wiek', fontsize=14)
#     ax.set_ylabel('Liczba członków', fontsize=14)
#     st.pyplot(fig)
#     for club in AgesButDictionary:
#         if len(AgesButDictionary[club]) > 1:
#             avgAge = mean(AgesButDictionary[club])
#             st.write(
#                 f"Dla klubu {club} w {term} kandecji sejmu najstarszy członek miał {max(AgesButDictionary[club])} lat, najmłodszy miał {min(AgesButDictionary[club]) } lat, średnia wieku wynosiła {round(avgAge)} lat, mediana wynosiła {median(AgesButDictionary[club])} lat, odchylenie standardowe wynosiło około {round(stdev(AgesButDictionary[club]))} lat")
#     st.header(
#         "Wykresy rozkłądu wieku klubów ")
#     for club in AgesButDictionary:
#         fig, ax = plt.subplots(figsize=(10, 6))
#         if len(AgesButDictionary[club]) > 2:
#             ax.hist(AgesButDictionary[club], bins=10,
#                     color='red', edgecolor='black')
#             ax.set_title(
#                 f'Ogólny rozkład wiekowy klubu {club} dla {term} kadencji sejmu', fontsize=16)
#             ax.set_xlabel('Wiek', fontsize=14)
#             ax.set_ylabel('Liczba członków', fontsize=14)
#             st.pyplot(fig)


def loadView():
    # term = 10
    # searchedInfo = 'edukacja'

    # st.markdown("hwilowo nic")
    MpGroupedList, MpsList, MpNamesByClub = MPsStats.groupMpsByClub(10)
    # ageDataframe, ageDictionary = MPsStats.ageStats(
    #     term, MpGroupedList, MpsList)
    # all_ages = ageDataframe.values.flatten()
    # all_ages = pd.Series(all_ages).dropna()
    # _sharedViews.ageGraphs(all_ages, ageDictionary, term)
    # educationDictionary = MPsStats.MoreMPsStats(
    #     MpsList, MpGroupedList, term, searchedInfo)
    # _sharedViews.MoreStats(educationDictionary)
    term_number = st.number_input(
        "kadencja sejmu", min_value=1, value=10)
    stats = st.selectbox(
        "Wybierz stytystykę", ["brak", "wiek", "edukacja", "okrąg", "profesja",  "województwo"])
    match stats:
        case "brak":
            st.write("")
        case "wiek":
            ageDataframe, ageDictionary = MPsStats.ageStats(
                term_number, MpGroupedList, MpsList)
            all_ages = ageDataframe.values.flatten()
            all_ages = pd.Series(all_ages).dropna()
            _sharedViews.ageGraphs(all_ages, ageDictionary, term_number)
        case "edukacja":
            MPDictionary = MPsStats.MoreMPsStats(
                MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)
        case "profesja":
            MPDictionary = MPsStats.MoreMPsStats(
                MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)

        case "okrąg":
            MPDictionary = MPsStats.MoreMPsStats(
                MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)
        case "województwo":
            PDictionary = MPsStats.MoreMPsStats(
                MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)
    selectedMp = st.selectbox("Wybierz posła ",  list(
        mp['lastFirstName'] for mp in MpsList))
    HisotryOfMP = MPsStats.HistoryOfMp(selectedMp, MpsList)
