# import streamlit as st
# from Controller import electionCalc
# import pandas as pd
# # import numpy as np

# # st.set_page_config(layout="wide")


# def loadView():
#     # year = "2023"
#     threshold, methodSelect, parties = st.columns(3)
#     with threshold:
#         voteingThreshold = st.number_input("próg wyborczy", 0, 100)
#         voteingThresholdForCoaliton = st.number_input(
#             "próg wyborczy dla kolalicji", 0, 100)
#     # st.write(electionCalc.calculateVotes(voteingThreshold))
#     with methodSelect:
#         # method = st.selectbox("metoda liczenia głosów", [
#         #     "d'Hondt", "Sainte-Laguë", "Zmodyfikowany Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
#         year = st.selectbox("wybierz instersujce cię wybory", [
#                             "2023", "2019", "2015", "2011", "2007", "2005", "2001"])

#     qulifiedParties, allParitesDict, voteForDistrict = electionCalc.calculateVotes(
#         voteingThreshold, voteingThresholdForCoaliton, year)
#     allPrtiesDict2 = allParitesDict.copy()
#     with parties:
#         st.write("Wybierz czy partia ma być zwolniona z progu wyborczgo")
#         with st.container(height=300):
#             for key in allParitesDict:
#                 if key != "Frekwencja":
#                     allParitesDict[key] = st.checkbox(f"{key}", False)
#             # Don't bloat terminal
#             # print(allParitesDict)
#             # w przyszłości jak zrobię lub ktoś zorobi słownik z wszysttkimi nazwami koitetów i ich krótami to się zastąpi

#     # st.write(electionCalc.calculateVotes(voteingThreshold))
#     for key in allParitesDict:
#         if key != "Frekwencja" and allParitesDict[key] is True and key not in qulifiedParties:
#             qulifiedParties.append(key)
#             # ilość głosów tylko jej narzie nigdzie nie zwracam
#     results = electionCalc.chooseMethod(
#         qulifiedParties, voteForDistrict, year)

#     # for party in results[key]:
#     # if results[key][party] > 0:
#     #     st.write(f" {party}: {results[key][party]}")

#     filtered_results = {}
#     for key in results.keys():
#         filtered_results[key] = {party: votes for party,
#                                  votes in results[key].items() if votes != 0}
#         # st.write(f"{key}: ")

#     FiltredResultsDF = pd.DataFrame.from_dict(filtered_results)
#     FiltredResultsDF = FiltredResultsDF.fillna(value=" ")
#     FiltredResultsDF = FiltredResultsDF.astype(str)
#     FiltredResultsDF = FiltredResultsDF.replace(r'\.0$', ' ', regex=True)

#     # st.table(FiltredResultsDF)

#     FiltredResultsDF = FiltredResultsDF.transpose()
#     st.table(FiltredResultsDF)
