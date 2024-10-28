import streamlit as st
import matplotlib.pyplot as plt

from Controller.Commitees import CommiteesList, CommiteeFutureSetting, LastNCommitteeSettingDates
import json
from Controller.Results import getResults


def loadView():
    st.header("komisje")
    term_number = st.number_input(
        "Numer Kadencji", value=10, placeholder="Wpisz numer"
    )

    commitees = CommiteesList(term_number)
    for commitee in commitees:
        st.markdown(
            f"{commitee['name']} o kodzie: {commitee['code']}")

    committeeCode = st.text_input(
        "Kod komisij", value="ASW", placeholder="Podaj kod komisji")
    st.markdown(
        f"posiedzenia wybranej komisji w ciągu ostanich 3 dni,{CommiteeFutureSetting(term_number,committeeCode)}")
    numberOfSettings = st.number_input(
        "ile ostanich posiedzień komijsji cię interesuje", 1, value=1)
    settingsList = LastNCommitteeSettingDates(
        committeeCode, numberOfSettings, term_number)
    st.markdown(
        f"ostanie {numberOfSettings} posiedzeń komijsji miały miejsce,{settingsList}")
    # correlationValue = st.number_input(
    #    label="Podaj jak bardzo wartości mają być skorelowane [-1;1]", min_value=-1.0, max_value=1.0)
    type = st.selectbox("Wybierz rodzaj analizowanych wyników",
                        ("procętowe", "ilościowe"))
    correlationValue = -1
    electionSelections = st.selectbox("wybierz poziom administracyjny do analizy ", (
        "województwa", "okręgi", "powiaty", "gminy", "obwody"))
    matrix, Results = getResults(correlationValue, electionSelections, type)
    st.dataframe(matrix)

    axisX = st.selectbox("wybierz pierwszy element korelacji",
                         Results.columns)
    axisY = st.selectbox("wybierz drugi element korelacji",
                         Results.columns)

    fig, ax = plt.subplots()
    st.write(f"korelacja między {axisX, axisY}")
    ax.scatter(Results[axisX], Results[axisY],
               color='blue', marker='o')
    # Oznaczenie osi i tytuł wykresu
    ax.set_xlabel(axisX)
    ax.set_ylabel(axisY)

    ax.legend()

    # Wyświetlenie wykresu w aplikacji
    st.pyplot(fig)
