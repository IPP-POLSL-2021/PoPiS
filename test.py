from streamlit_push_notifications import send_push
import streamlit as st
import matplotlib.pyplot as plt

from Committee.Commitees import CommiteesList, CommiteeFutureSetting
import json
from Results.Results import getResults
st.header("komisije")
term_number = st.number_input(
    "Numer Kadencji", value=10, placeholder="Wpisz numer"
)
commitees = CommiteesList(term_number)
for commite in commitees:
    st.markdown(
        f"{commite['name']} o kodzie: {commite['code']}")
committeeCode = st.text_input(
    "Kod komisij", value="ASW", placeholder="Podaj kod komisji")

st.markdown(
    f"nasępne posiedzenie wybranej komisiji,{CommiteeFutureSetting(term_number,committeeCode)}")
correlationValue = st.number_input(
    label="Podaj jak bardzo wartości mają być skorelowane [-1;1]", min_value=-1.0, max_value=1.0)
type = st.selectbox("Wybierz rodzaj analizowanych wyników",
                    ("procętowe", "ilościowe"))
electionSelections = st.selectbox("wybierz poziom admistracyjny do analzy ", (
    "województwa", "okręgi", "powiaty", "gminy", "obwody"))
matrix, Results = getResults(correlationValue, electionSelections, type)
st.dataframe(matrix)

axisX = st.selectbox("wybierz pierwszy elemnt korelacji",
                     Results.columns)
axisY = st.selectbox("wybierz drugi elemnt korelacji",
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
