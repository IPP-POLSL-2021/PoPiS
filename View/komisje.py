import streamlit as st
from api_wrappers.committees import get_committees, get_committee_future_sitting, get_last_n_committee_sitting_dates

def loadView():
    st.header("Komisje Sejmowe")
    
    term_number = st.number_input(
        "Numer Kadencji", value=10, placeholder="Wpisz numer"
    )

    # Get committees and handle empty list scenario
    committees = get_committees(term_number)
    
    if not committees:
        st.warning(f"Nie znaleziono komisji dla kadencji {term_number}")
        return

    # Create committee codes with fallback
    codes = [
        f"{committee['name']} & {committee['code']}" for committee in committees
    ]

    # Add a default option
    codes.insert(0, "Wybierz komisję")

    selectedCommittee = st.selectbox(
        "Wybierz komisję", 
        options=codes,
        index=0  # Default to first option
    )

    # Check if a real committee is selected
    if selectedCommittee == "Wybierz komisję":
        st.info("Proszę wybrać komisję z listy")
        return

    # Safely extract committee code
    committeeCode = selectedCommittee.split("&")[-1].strip()

    # Days input
    days = st.number_input(
        "Z ilu ostatnich dni chcesz zobaczyć posiedzenia", 
        min_value=1, 
        value=3
    )   

    # Future sittings
    future_sittings = get_committee_future_sitting(term_number, committeeCode, days)
    st.markdown(f"Posiedzenia wybranej komisji w ciągu ostatnich {days} dni:")
    st.write(future_sittings)

    # Number of past sittings
    numberOfSettings = st.number_input(
        "Ilość ostatnich posiedzeń komisji, które chcesz zobaczyć", 
        min_value=1, 
        value=1
    )

    # Past sittings
    settingsList = get_last_n_committee_sitting_dates(
        committeeCode, numberOfSettings, term_number
    )
    st.markdown(f"Ostatnie {numberOfSettings} posiedzeń komisji:")
    st.write(settingsList)
