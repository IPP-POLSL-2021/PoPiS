from api_wrappers.committees import get_committee_stats, get_committees, get_committee_member_ages, get_committee_member_details
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from statistics import mean, median, stdev
from View import _sharedViews
from st_aggrid import AgGrid


def loadView():
    term_number = st.number_input(
        "kadencja sejmu", min_value=1, value=10)

    codes = [
        f"{committee['name']} - {committee['code']}" for committee in get_committees(term_number)]
    codes.append("łącznie")
    selectedCommittee = st.selectbox(
        "komisja której statystyki cię interesują (niektóre dostępne tylko dla obecnej kadencji)", options=list(codes)
    )
    if selectedCommittee != "łącznie":
        selectedCommittee = selectedCommittee.split("-")[-1][1:]
    committee_stats = get_committee_stats(term_number, selectedCommittee)
    clubs = pd.DataFrame.from_dict(committee_stats['clubs'], orient='index')
    MPs = pd.DataFrame.from_dict(committee_stats['members'], orient='index')
    clubsButBetter = committee_stats['clubs']

    ClubsCount = clubs.apply(lambda x: x.count(), axis=1)

    # Plotly bar chart for ClubsCount
    fig = px.bar(
        ClubsCount,
        x=ClubsCount.index,
        y=ClubsCount.values,
        title='Liczba członków w komisjach',
        labels={'x': 'Partie', 'y': 'Liczba członków'}
    )
    fig.update_layout(
        xaxis_title='Partie',
        yaxis_title='Liczba członków',
        title_font_size=16,
        xaxis_tickangle=45
    )
    st.plotly_chart(fig)
    clubs.columns = [str(col).replace('.', '_') for col in clubs.columns]

    AgGrid(clubs)
    # st.dataframe(clubs, use_container_width=True)
    # if selectedCommittee == "łącznie":
    #    MPs.columns = [str(col).replace('.', '_') for col in MPs.columns]
    #    AgGrid(MPs)
    if selectedCommittee == "łącznie":
        st.dataframe(MPs, use_container_width=True)

    DataframeAges, AgesButDictionary = get_committee_member_ages(
        clubsButBetter, term_number)
    all_ages = DataframeAges.values.flatten()
    all_ages = pd.Series(all_ages).dropna()

    # Statistics selection
    stats = st.selectbox(
        "Wybierz statystykę", ["brak", "wiek", "edukacja",  "profesja"]
    )
    match stats:
        case "wiek":
            _sharedViews.ageGraphs(all_ages, AgesButDictionary, term_number)
        case "edukacja":
            EducationDictionary = get_committee_member_details(
                clubsButBetter, term_number, 'edukacja')
            _sharedViews.MoreStats(EducationDictionary)
        case "profesja":
            EducationDictionary = get_committee_member_details(
                clubsButBetter, term_number, 'profesja')
            _sharedViews.MoreStats(EducationDictionary)
        case "brak":
            st.write("")
