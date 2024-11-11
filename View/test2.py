import streamlit as st
import matplotlib.pyplot as plt

from api_wrappers.committees import get_committees, get_committee_future_sitting, get_last_n_committee_sitting_dates
import json
from Controller.Results import getResults


def loadView():
    st.header("komisje")
    term_number = st.number_input(
        "Numer Kadencji", value=10, placeholder="Wpisz numer"
    )

    committees = get_committees(term_number)
    for committee in committees:
        st.markdown(
            f"{committee['name']} o kodzie: {committee['code']}")

    committeeCode = st.text_input(
        "Kod komisji", value="ASW", placeholder="Podaj kod komisji")
    st.markdown(
        f"Posiedzenia wybranej komisji w ciągu ostatnich 3 dni,{get_committee_future_sitting(term_number,committeeCode)}")
    numberOfSettings = st.number_input(
        "Ilość ostatnich posiedzień komisji które chcesz zobaczyć", 1, value=1)
    settingsList = get_last_n_committee_sitting_dates(
        committeeCode, numberOfSettings, term_number)
    st.markdown(
        f"ostatnie {numberOfSettings} posiedzeń komisji miały miejsce,{settingsList}")
    # correlationValue = st.number_input(
    #    label="Podaj jak bardzo wartości mają być skorelowane [-1;1]", min_value=-1.0, max_value=1.0)
    type = st.selectbox("Wybierz rodzaj analizowanych wyników",
                        ("procentowe", "ilościowe"))
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
