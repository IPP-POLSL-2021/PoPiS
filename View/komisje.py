import streamlit as st
from api_wrappers.committees import get_committees, get_committee_future_sitting, get_last_n_committee_sitting_dates
import requests
# from View import committeeTranscript


def loadView():
    st.header("Komisje Sejmowe")

    term_number = st.number_input(
        "Numer Kadencji", min_value=3, value=10, placeholder="Wpisz numer"
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

    for committee in committees:
        if committee['code'] == committeeCode:
            if committee["appointmentDate"] == committee["compositionDate"]:
                st.write(
                    f"Komisja rozpoczęła działalność {committee['appointmentDate']}")
            else:
                st.write(
                    f"Komisja powołana {committee['appointmentDate']} a skład wybrany {committee['compositionDate']}")
            scope = committee.get("scope", False)
            if scope:
                with st.expander("Pokaż zakres działania komisji"):
                    st.write(scope)
            with st.expander("Pokaż prezydium komisji"):
                members = list()
                for member in committee['members']:
                    if member.get("function", False):
                        members.append(
                            tuple((member['function'], member['lastFirstName'], member['club'])))
                st.dataframe(sorted(members))

    if get_last_n_committee_sitting_dates(committeeCode, 1, term_number):
        col1, col2 = st.columns(2)

        with col1:
            # Days input
            if term_number == 10:
                days = st.number_input(
                    "Z ilu ostatnich dni chcesz zobaczyć posiedzenia",
                    min_value=1,
                    value=3
                )

            # Future sittings
                future_sittings = get_committee_future_sitting(
                    term_number, committeeCode, days, True)
                if future_sittings:
                    st.markdown(
                        f"Posiedzenia wybranej komisji w ciągu ostatnich {days} dni:")
                    # future_sittings = pd.DataFrame(future_sittings)
                    # future_sittings = future_sittings.values.tolist()
                    st.table(future_sittings)
                else:
                    st.write(
                        f"W ciągu ostatnich {days} dni nie było posiedzenia")
            else:
                st.write(
                    f"Komisja zakończyła działalność {get_last_n_committee_sitting_dates(committeeCode, 1,term_number)[0]}")
        with col2:
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

            # selectedSetting = st.selectbox(
            #     f"Ostatnie {numberOfSettings} posiedzeń komisji:", settingsList)
            for setting in settingsList:
                # st.write(setting)
                nthSetting = setting.split(":")
                nthSetting = nthSetting[-1][1:]
            # if selectedSetting != "brak" or selectedSetting != "":
                with st.expander(f"Posiedzenie nr {nthSetting} - {selectedCommittee}"):
                    # print("e")
                    request = requests.get(
                        f"https://api.sejm.gov.pl/sejm/term{term_number}/committees/{committeeCode}/sittings/{nthSetting}")
                    response = request.json()
                    st.html(response["agenda"])
                    # if st.button(f"Pokaż transkrypt posiedzenia nr {nthSetting}"):
                    #     committeeTranscript.loadView(
                    #         term_number, committeeCode, nthSetting)
                    if requests.get(f"https://api.sejm.gov.pl/sejm/term{term_number}/committees/{committeeCode}/sittings/{nthSetting}/html"):
                        st.markdown(
                            f"[Transkrypcja posiedzenia](https://api.sejm.gov.pl/sejm/term{term_number}/committees/{committeeCode}/sittings/{nthSetting}/html)", unsafe_allow_html=True)
                    else:
                        st.write("Brak dostępnego transkryptu.")
                # print(nthSetting)
    else:
        st.write("Brak danych o posiedzeniach komisji")
