import streamlit as st
from Controller import MPsStats
import pandas as pd
from View import _sharedViews
import numpy as np


def loadView():
    term_number = st.number_input("kadencja sejmu", min_value=1, value=10)
    MpGroupedList, MpsList, MpNamesByClub = MPsStats.groupMpsByClub(
        term_number)
    stats = st.selectbox(
        "Wybierz statystykę", ["brak", "wiek",
                               "edukacja", "okrąg", "profesja", "województwo"]
    )

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

            # _sharedViews.MoreStats(MPDictionary)
            reversedMPDict = {}
            # for key, value in MPDictionary.items():
            #     reversedMPDict[value] = key

            MPDataFrame = pd.DataFrame.from_dict(MPDictionary)
            MPDataFrame = MPDataFrame.fillna(value=" ")
            MPDataFrame = MPDataFrame.astype(str)
            MPDataFrame = MPDataFrame.replace(r'\.0$', '', regex=True)
            st.dataframe(MPDataFrame)
        case "województwo":
            MPDictionary = MPsStats.MoreMPsStats(
                MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)

    selectedMp = st.selectbox("Wybierz posła ", list(
        mp['lastFirstName'] for mp in MpsList))
    HistoryOfMP = MPsStats.HistoryOfMp(selectedMp, MpsList, term_number)

    data = []
    total_votes = 0

    for term in HistoryOfMP:
        obj = HistoryOfMP[term]
        total_votes += obj.numberOfVotes
        data.append({
            "Kadencja": term,
            "Klub": obj.club,
            "Okrąg": obj.districtName,
            "Województwo": obj.voivodeship if len(str(obj.voivodeship)) > 4 else "Brak danych",
            "Edukacja": getattr(obj, "educationLevel", "Brak danych"),
            "Uzyskane głosy": obj.numberOfVotes if obj.numberOfVotes > 0 else "Brak danych",
            "Profesja": obj.profession if obj.profession else "Brak danych"
        })
    club = ""
    if len(set(d['Klub'] for d in data)) == 1:
        club = "unikalny klub"
    else:
        club = "unikalne kluby"
    district = ""
    if len(set(d['Województwo'] for d in data if d['Województwo'] is not None)) == 1:
        district = "unikalny okrąg"
    else:
        district = "unikalne okręgi"
    voivodiship = ""
    if len(set(d['Województwo'] for d in data if d['Województwo'] is not None)) == 1:
        voivodiship = "unikalny poziom edukacji"
    else:
        voivodiship = "unikalne poziomy edukacji"
    edu = ""
    if {len(set(d['Edukacja'] for d in data if d['Edukacja'] != 'None'))} == 1:
        edu = "unikalne województwo"
    else:
        edu = "unikalne województwa"

    prof = ""
    if len(set(d['Profesja'] for d in data if d['Profesja'] != 'None')) == 1:
        prof = "unikalny zawód"
    else:
        prof = "unikalne zawody"
    data.append({
        "Kadencja": "Łącznie",
        "Klub": f"{len(set(d['Klub'] for d in data))} {club} ",
        "Okrąg": f"{len(set(d['Okrąg'] for d in data))} {district}",
        "Województwo": f"{len(set(d['Województwo'] for d in data if d['Województwo'] is not None))} {voivodiship}",
        "Edukacja": f"{len(set(d['Edukacja'] for d in data if d['Edukacja'] != 'None'))} {edu}",
        "Uzyskane głosy": total_votes,
        "Profesja": f"{len(set(d['Profesja'] for d in data if d['Profesja'] != 'None'))} {prof}"
    })

    summary_df = pd.DataFrame(data)
    st.table(summary_df)
