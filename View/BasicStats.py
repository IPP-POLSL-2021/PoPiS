import streamlit as st
from Controller import MPsStats
import pandas as pd
from View import _sharedViews

def loadView():
    MpGroupedList, MpsList, MpNamesByClub = MPsStats.groupMpsByClub(10)
    term_number = st.number_input("kadencja sejmu", min_value=1, value=10)
    stats = st.selectbox(
        "Wybierz statystykę", ["brak", "wiek", "edukacja", "okrąg", "profesja", "województwo"]
    )
    
    match stats:
        case "brak":
            st.write("")
        case "wiek":
            ageDataframe, ageDictionary = MPsStats.ageStats(term_number, MpGroupedList, MpsList)
            all_ages = ageDataframe.values.flatten()
            all_ages = pd.Series(all_ages).dropna()
            _sharedViews.ageGraphs(all_ages, ageDictionary, term_number)
        case "edukacja":
            MPDictionary = MPsStats.MoreMPsStats(MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)
        case "profesja":
            MPDictionary = MPsStats.MoreMPsStats(MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)
        case "okrąg":
            MPDictionary = MPsStats.MoreMPsStats(MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)
        case "województwo":
            MPDictionary = MPsStats.MoreMPsStats(MpsList, MpGroupedList, term_number, stats)
            _sharedViews.MoreStats(MPDictionary)

    selectedMp = st.selectbox("Wybierz posła ", list(mp['lastFirstName'] for mp in MpsList))
    HistoryOfMP = MPsStats.HistoryOfMp(selectedMp, MpsList)
    
    data = []
    total_votes = 0
    
    for term in HistoryOfMP:
        obj = HistoryOfMP[term]
        total_votes += obj.numberOfVotes
        data.append({
            "Term": term,
            "Club": obj.club,
            "District": obj.districtName,
            "Voivodeship": obj.voivodeship,
            "Education": getattr(obj, "educationLevel", "N/A"),
            "Votes": obj.numberOfVotes if obj.numberOfVotes > 0 else "N/A",
            "Profession": obj.profession if obj.profession else "None"
        })

    data.append({
        "Term": "Total",
        "Club": f"{len(set(d['Club'] for d in data))} unique clubs",
        "District": f"{len(set(d['District'] for d in data))} unique districts",
        "Voivodeship": f"{len(set(d['Voivodeship'] for d in data if d['Voivodeship'] is not None))} unique voivodeships",
        "Education": f"{len(set(d['Education'] for d in data if d['Education'] != 'None'))} unique education",
        "Votes": total_votes,
        "Profession": f"{len(set(d['Profession'] for d in data if d['Profession'] != 'None'))} unique professions"
    })
    
    summary_df = pd.DataFrame(data)
    st.table(summary_df)
