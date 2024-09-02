from streamlit_push_notifications import send_push
import streamlit as st
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
electionSelections = st.selectbox("wybierz poziom admistracyjny do analzy ", (
    "województwa", "okręgi", "powiaty", "gminy", "obwody"))
st.dataframe(getResults(correlationValue, electionSelections))
