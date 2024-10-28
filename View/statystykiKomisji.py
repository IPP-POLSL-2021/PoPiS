from Controller.Commitees import ComitteStats, CommiteesList, CommitteeAge, ComitteEducation
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import mean, median, stdev


def ageStats(all_ages, AgesButDictionary):
    print("a")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(all_ages, bins=10, color='red', edgecolor='black')
    ax.set_title('Ogólny rozkład wiekowy członków komisji', fontsize=16)
    ax.set_xlabel('Wiek', fontsize=14)
    ax.set_ylabel('Liczba członków', fontsize=14)
    st.pyplot(fig)
    for club in AgesButDictionary:
        if len(AgesButDictionary[club]) > 1:
            avgAge = mean(AgesButDictionary[club])
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


def MoreStats(ChosenDictionary):
    st.write(
        "wykresy dla klubów w komijsch gdzie cczłonkiwe mają rózne wykształcenie")
    for club in ChosenDictionary:
        if len(list(ChosenDictionary[club].keys())) > 1:
            fig, ax = plt.subplots(figsize=(10, 5))
            labels = list(ChosenDictionary[club].keys())
            values = list(ChosenDictionary[club].values())
            ax.pie(values, labels=labels)
            ax.set_title(
                f'Ogólny rozkład edukacji członków komisji dla klubu {club}', fontsize=16)

            st.pyplot(fig)


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
    stats = st.selectbox(
        "Wybierz stytystykę", ["brak", "wiek", "edukacja", "okrąg", "profesja",  "województwo"])
    match stats:
        case "wiek":
            ageStats(all_ages, AgesButDictionary)
        case "edukacja":
            EducationDictionary = ComitteEducation(
                clubsButBetter, term_number, stats)
            MoreStats(EducationDictionary)
        case "profesja":
            EducationDictionary = ComitteEducation(
                clubsButBetter, term_number, stats)
            MoreStats(EducationDictionary)
        case "okrąg":
            EducationDictionary = ComitteEducation(
                clubsButBetter, term_number, stats)
            MoreStats(EducationDictionary)
        case "województwo":
            EducationDictionary = ComitteEducation(
                clubsButBetter, term_number, stats)
            MoreStats(EducationDictionary)

            MoreStats(EducationDictionary)
        case "brak":
            st.write("")
