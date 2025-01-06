import streamlit as st
import plotly.express as px
from Controller.Results import getResults

def loadView():
    # Add default options and info messages for each selectbox
    type = st.selectbox("Wybierz rodzaj analizowanych wyników",
                        ["Wybierz rodzaj"] + ["procentowe", "ilościowe"])

    if type == "Wybierz rodzaj":
        st.info("Wybierz rodzaj analizowanych wyników")
        return

    correlationValue = -1

    electionSelections = st.selectbox(
        "Wybierz poziom administracyjny do analizy",
        ["Wybierz poziom"] + ["województwa", "okręgi", "powiaty", "gminy", "obwody"]
    )

    if electionSelections == "Wybierz poziom":
        st.info("Wybierz poziom administracyjny")
        return

    matrix, Results = getResults(correlationValue, electionSelections, type)
    matrix = matrix.fillna(0.0)

    datafreame_col, plot_col = st.tabs([
        "Macierz korelacji", "Wykres"])

    with datafreame_col:
        st.dataframe(matrix)

    with plot_col:
        # Add default option for first correlation element
        axisX_options = ["Wybierz pierwszy element"] + list(Results.columns)
        axisX = st.selectbox("Wybierz pierwszy element korelacji", axisX_options)

        if axisX == "Wybierz pierwszy element":
            st.info("Wybierz pierwszy element korelacji")
            return

        # Filter options for second element to exclude the first selection
        columns_2 = Results.columns.copy()
        columns_2 = columns_2.drop(axisX)

        # Add default option for second correlation element
        axisY_options = ["Wybierz drugi element"] + list(columns_2)
        axisY = st.selectbox("Wybierz drugi element korelacji", axisY_options)

        if axisY == "Wybierz drugi element":
            st.info("Wybierz drugi element korelacji")
            return

        reggresionLine = st.checkbox("Czy pokazać linię regresji")
        Results = Results[Results[axisX] > 0]

        if not reggresionLine:
            fig = px.scatter(Results, x=axisX, y=axisY)
        elif reggresionLine and electionSelections == "obwody":
            fig = px.scatter(Results, x=axisX, y=axisY,
                             trendline="ols", trendline_color_override="green")
        else:
            fig = px.scatter(Results, x=axisX, y=axisY,
                             trendline="ols", trendline_options=dict(log_x=True), trendline_color_override="green")

        st.plotly_chart(fig)
