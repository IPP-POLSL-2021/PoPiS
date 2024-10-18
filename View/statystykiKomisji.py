from Controller.Commitees import ComitteStats, CommiteesList, CommitteeAge
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean, median, stdev


def loadView():
    term_number = st.number_input(
        "kadencja sejmu", min_value=1, value=10)
    # print("puki co psuto")

    codes = [committee['code'] for committee in CommiteesList(term_number)]
    codes.append("łącznie")
    selectedCommittee = st.selectbox(
        "komijsja której statyski cię intersują (niektóre dostępne tylko dla obecnej kadecji)", options=list(codes)
    )

    clubs, MPs, clubsButBetter = ComitteStats(term_number, selectedCommittee)
    # with st.container(height=400):
    #     for MP in MPs:
    #         st.markdown(MP)
    # wyświetlanie informacji o ilości członkó i ilości komijsi
    ClubsCount = clubs.apply(lambda x: x.count(), axis=1)

    fig, ax = plt.subplots(figsize=(10, 6))
    ClubsCount.plot(kind='bar', ax=ax)
    ax.set_title('Liczba członków w komisjach', fontsize=16)

    ax.set_xlabel('Partie', fontsize=14)
    ax.set_ylabel('Liczba członków', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    st.dataframe(clubs)
    if selectedCommittee == "łącznie":
        st.dataframe(MPs)
    # wykresy wieku
    DataframeAges, AgesButDictionary = CommitteeAge(
        clubsButBetter, term_number)
    all_ages = DataframeAges.values.flatten()
    all_ages = pd.Series(all_ages).dropna()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(all_ages, bins=10, color='red', edgecolor='black')
    ax.set_title('Ogólny rozkład wiekowy członków komisji', fontsize=16)
    ax.set_xlabel('Wiek', fontsize=14)
    ax.set_ylabel('Liczba członków', fontsize=14)
    st.pyplot(fig)
    for club in AgesButDictionary:
        avgAge = mean(AgesButDictionary[club])
        if len(AgesButDictionary[club]) > 1:
            st.write(
                f"Dla klubu {club} w wybrnej komisji najstarszy członek ma {max(AgesButDictionary[club])} lat, najmłodszy ma {min(AgesButDictionary[club]) } lat, średnia wieku wynosi {round(avgAge)} lat, mediana wynosi {median(AgesButDictionary[club])} lat, odchylenie standardowe wynosi około {round(stdev(AgesButDictionary[club]))} lat")
    st.header(
        "Wykresy rozkłądu wieku klubów dla wybranej komisji jeśli dany klub ma więcej niż2 członków")
    for club in AgesButDictionary:
        fig, ax = plt.subplots(figsize=(10, 6))
        if len(AgesButDictionary[club]) > 2:
            ax.hist(AgesButDictionary[club], bins=10,
                    color='red', edgecolor='black')
            ax.set_title(
                f'Ogólny rozkład wiekowy członków komisji dla klubu {club}', fontsize=16)
            ax.set_xlabel('Wiek', fontsize=14)
            ax.set_ylabel('Liczba członków', fontsize=14)
            st.pyplot(fig)
