from streamlit_push_notifications import send_push
import streamlit as st
from Committee.Commitees import CommiteesList, CommiteeFutureSetting
import json
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
