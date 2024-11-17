import streamlit as st
from Controller import electionCalc


def loadView():
    threshold, methodSelect, parties = st.columns(3)
    with threshold:
        voteingThreshold = st.number_input("próg wyborczy", 0, 100)
        voteingThresholdForCoaliton = st.number_input(
            "próg wyborczy dla kolalicji", 0, 100)
    # st.write(electionCalc.calculateVotes(voteingThreshold))

    qulifiedParties, allParitesDict, voteForDistrict = electionCalc.calculateVotes(
        voteingThreshold, voteingThresholdForCoaliton)
    with parties:
        st.write("Wybierz czy partia ma być zwolniona z progu wyborczgo")
        with st.container(height=300):
            for key in allParitesDict:
                if key != "Frekwencja":
                    allParitesDict[key] = st.checkbox(f"{key}", False)
            print(allParitesDict)
            # w przyszłości jak zrobię lub ktoś zorobi słownik z wszysttkimi nazwami koitetów i ich krótami to się zastąpi

    # st.write(electionCalc.calculateVotes(voteingThreshold))
    with methodSelect:
        method = st.selectbox("metoda liczenia głosów", [
            "d'Hondt", "Sainte-Laguë", "Kwota Hare’a (metoda największych reszt)", "Kwota Hare’a (metoda najmniejszych reszt)"])
    # for key in allParitesDict:
    #     if key != "Frekwencja" and allParitesDict[key] is True and key not in qulifiedParties.keys():
    #         qulifiedParties[key]= ilość głosów tylko jej narzie nigdzie nie zwracam
    results = electionCalc.chooseMethod(
        method, qulifiedParties, voteForDistrict)
    for key in results.keys():
        if results[key] > 0:
            st.write(f"{key}: {results[key]}")
