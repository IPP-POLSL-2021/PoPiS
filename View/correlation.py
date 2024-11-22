import streamlit as st
import matplotlib.pyplot as plt
import json
from Controller.Results import getResults


def loadView():
    # correlationValue = st.number_input(
    #    label="Podaj jak bardzo wartości mają być skorelowane [-1;1]", min_value=-1.0, max_value=1.0)
    type = st.selectbox("Wybierz rodzaj analizowanych wyników",
                        ("procentowe", "ilościowe"))
    correlationValue = -1
    electionSelections = st.selectbox("wybierz poziom administracyjny do analizy ", (
        "województwa", "okręgi", "powiaty", "gminy", "obwody"))
    matrix, Results = getResults(correlationValue, electionSelections, type)
    st.dataframe(matrix)

    axisX = st.selectbox("wybierz pierwszy element korelacji", Results.columns)
    axisY = st.selectbox("wybierz drugi element korelacji", Results.columns)

    fig, ax = plt.subplots()
    st.write(f"korelacja między {axisX, axisY}")
    ax.scatter(Results[axisX], Results[axisY], color='blue', marker='o')
    # Oznaczenie osi i tytuł wykresu
    ax.set_xlabel(axisX)
    ax.set_ylabel(axisY)

    ax.legend()

    # Wyświetlenie wykresu w aplikacji
    st.pyplot(fig)
