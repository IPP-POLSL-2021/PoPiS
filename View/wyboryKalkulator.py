import streamlit as st
from Controller import electionCalc


def loadView():
    st.write("narzie nic")
    voteingThreshold = st.number_input("próg wyborczy", 0, 100)
    qulifiedParties, votes = electionCalc.calculateVotes(voteingThreshold)
    st.write(electionCalc.calculateVotes(voteingThreshold))
    method = st.selectbox("metoda liczenia głosów", [
        "d'Hondt", "Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
    results = electionCalc.chooseMethod(method, qulifiedParties, votes)
    st.write(results)
