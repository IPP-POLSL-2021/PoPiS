import streamlit as st
from api_wrappers.committees import get_committees, get_committee_future_sitting, get_last_n_committee_sitting_dates

def loadView():
    st.header("komisje")
    term_number = st.number_input(
        "Numer Kadencji", value=10, placeholder="Wpisz numer"
    )

    codes = [
        f"{committee['name']} & {committee['code']}" for committee in get_committees(term_number)]

    selectedCommittee = st.selectbox(
        "Wybierz komisję", options=list(codes)
    )
    committeeCode = selectedCommittee.split("&")[-1][1:] 
    st.markdown(
        f"Posiedzenia wybranej komisji w ciągu ostatnich 3 dni,{get_committee_future_sitting(term_number,committeeCode)}")
    numberOfSettings = st.number_input(
        "Ilość ostatnich posiedzień komisji które chcesz zobaczyć", 1, value=1)
    settingsList = get_last_n_committee_sitting_dates(
        committeeCode, numberOfSettings, term_number)
    st.markdown(
        f"ostatnie {numberOfSettings} posiedzeń komisji miały miejsce,{settingsList}")
