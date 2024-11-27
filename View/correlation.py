import streamlit as st
import matplotlib.pyplot as plt
import json
from Controller.Results import getResults
import plotly.express as px
import plotly.graph_objects as go


def loadView():
    # correlationValue = st.number_input(
    #    label="Podaj jak bardzo wartości mają być skorelowane [-1;1]", min_value=-1.0, max_value=1.0)
    type = st.selectbox("Wybierz rodzaj analizowanych wyników",
                        ("procentowe", "ilościowe"))
    correlationValue = -1
    electionSelections = st.selectbox("wybierz poziom administracyjny do analizy ", (
        "województwa", "okręgi", "powiaty", "gminy", "obwody"))
    matrix, Results = getResults(correlationValue, electionSelections, type)
    datafreame_col, polot_col = st.columns([0.6, 0.4])
    with datafreame_col:
        st.dataframe(matrix)
    with polot_col:
        axisX = st.selectbox(
            "wybierz pierwszy element korelacji", Results.columns)
        columns_2 = Results.columns.copy()
        columns_2 = columns_2.drop(axisX)
        axisY = st.selectbox("wybierz drugi element korelacji", columns_2)

        # fig, ax = plt.subplots()
        # # st.write(f"korelacja między {axisX}, {axisY}")
        # ax.scatter(Results[axisX], Results[axisY], color='blue', marker='o')
        # # Oznaczenie osi i tytuł wykresu
        # ax.set_xlabel(axisX)
        # ax.set_ylabel(axisY)

        # ax.legend()

        # Wyświetlenie wykresu w aplikacji
        st.pyplot(fig)
        values = Results[axisX]
        fig = px.scatter(Results, x=axisX, y=axisY)
        # fig.update_layout(
        #     title=f"korelacja między {axisX}, {axisY}",
        # )
        st.plotly_chart(fig)
