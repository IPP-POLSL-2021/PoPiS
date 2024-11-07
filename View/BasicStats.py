import streamlit as st
from Controller import MPsStats
import pandas as pd
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
    term_number = st.number_input("kadencja sejmu", min_value=1, value=10)
    stats = st.selectbox(
        "Wybierz stytystykę", ["brak", "wiek", "edukacja", "okrąg", "profesja", "województwo"]
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
    HisotryOfMP = MPsStats.HistoryOfMp(selectedMp, MpsList)
    
    # Data structure to collect all rows for the table
    data = []
    total_votes = 0
    
    # Loop through each term in the MP's history
    for term in HisotryOfMP:
        obj = HisotryOfMP[term]
        
        # Accumulate total votes for summary row
        total_votes += obj.numberOfVotes
        
        # Append a row of data for this term
        data.append({
            "Term": term,
            "Club": obj.club,
            "District": obj.districtName,
            "Voivodeship": obj.voivodeship,
            "Education": getattr(obj, "educationLevel", "N/A"),  # Use "N/A" if education attribute is missing
            "Votes": obj.numberOfVotes if obj.numberOfVotes > 0 else "N/A",
            "Profession": obj.profession if obj.profession else "None"
        })

    # Add a summary (total) row
    data.append({
        "Term": "Total",
        "Club": f"{len(set(d['Club'] for d in data))} unique clubs",
        "District": f"{len(set(d['District'] for d in data))} unique districts",
        "Voivodeship": f"{len(set(d['Voivodeship'] for d in data if d['Voivodeship'] is not None))} unique voivodeships",
        "Education": f"{len(set(d['Education'] for d in data if d['Education'] != 'None'))} unique education",
        "Votes": total_votes,
        "Profession": f"{len(set(d['Profession'] for d in data if d['Profession'] != 'None'))} unique professions"
    })
    
    # Convert data to a DataFrame and display as a table
    summary_df = pd.DataFrame(data)
    st.table(summary_df)
