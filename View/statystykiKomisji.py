from Controller.Commitees import ComitteStats, CommiteesList, CommitteeAge
import streamlit as st


def loadView():
    term_number = st.number_input(
        "kadencja sejmu", min_value=1, value=10)
    # print("puki co psuto")

    codes = [committee['code'] for committee in CommiteesList(term_number)]
    codes.append("łącznie")
    selectedCommittee = st.selectbox(
        "komijsja której statyski cię intersują (niektóre dostępne tylko dla obecnej kadecji)", options=list(codes)
    )

    clubs, MPs, clubsButBetter = ComitteStats(term_number, selectedCommittee)
    # with st.container(height=400):
    #     for MP in MPs:
    #         st.markdown(MP)
    st.dataframe(clubs)
    st.dataframe(MPs)
    CommitteeAge(clubsButBetter)
