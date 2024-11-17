import streamlit as st
from Controller import electionCalc


def loadView():

    voteingThreshold = st.number_input("próg wyborczy", 0, 100)
    voteingThresholdForCoaliton = st.number_input(
        "próg wyborczy dla kolalicji", 0, 100)
    # st.write(electionCalc.calculateVotes(voteingThreshold))
    qulifiedParties, votes, voteForDistrict = electionCalc.calculateVotes(
        voteingThreshold, voteingThresholdForCoaliton)
    # st.write(electionCalc.calculateVotes(voteingThreshold))
    method = st.selectbox("metoda liczenia głosów", [
        "d'Hondt", "Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
    results = electionCalc.chooseMethod(
        method, qulifiedParties, voteForDistrict)
    for key in results.keys():
        if results[key] > 0:
            st.write(f"{key}: {results[key]}")
