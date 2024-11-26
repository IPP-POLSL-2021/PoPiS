from api_wrappers.committees import get_committee_stats, get_committees, get_committee_member_ages, get_committee_member_details
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from statistics import mean, median, stdev
from View import _sharedViews
from st_aggrid import AgGrid
st.set_page_config(page_title="DataFrame Demo", page_icon="📊")


def loadView():
    term_number = st.number_input(
        "Kadencja sejmu", min_value=1, value=10, key='term_input_stats')

    codes = [
        f"{committee['name']} - {committee['code']}" for committee in get_committees(term_number)]
    codes.append("łącznie")
    selectedCommittee = st.selectbox(
        "Komisja, której statystyki cię interesują",
        options=list(codes),
        key='committee_select_stats'
    )

    if selectedCommittee != "łącznie":
        selectedCommittee = selectedCommittee.split("-")[-1][1:]

    committee_stats = get_committee_stats(term_number, selectedCommittee)
    clubs = pd.DataFrame.from_dict(committee_stats['clubs'], orient='index')
    MPs = pd.DataFrame.from_dict(committee_stats['members'], orient='index')
    clubsButBetter = committee_stats['clubs']

    # Prepare data for plotting
    ClubsCount = clubs.apply(lambda x: x.count(), axis=1)
    ClubsCountDF = pd.DataFrame({
        'Partie': ClubsCount.index,
        'Liczba członków': ClubsCount.values
    })

    # Plotly bar chart for ClubsCount
    fig = px.bar(
        ClubsCountDF,
        x='Partie',
        y='Liczba członków',
        title='Liczba członków w komisjach',
        labels={'Partie': 'Partie', 'Liczba członków': 'Liczba członków'}
    )
    fig.update_layout(
        xaxis_title='Partie',
        yaxis_title='Liczba członków',
        title_font_size=16,
        xaxis_tickangle=45
    )
    st.plotly_chart(fig)

    # Clean column names
    clubs.columns = [str(col).replace('.', '_') for col in clubs.columns]

    # Display clubs data
    AgGrid(clubs)

    # Display MPs data if "łącznie" is selected
    if selectedCommittee == "łącznie":
        st.dataframe(MPs, use_container_width=True)

    # Age and other statistics
    DataframeAges, AgesButDictionary = get_committee_member_ages(
        clubsButBetter, term_number)
    all_ages = DataframeAges.values.flatten()
    all_ages = pd.Series(all_ages).dropna()

    # Statistics selection
    stats = st.selectbox(
        "Wybierz statystykę",
        ["brak", "wiek", "edukacja", "profesja"],
        key='stats_select'
    )

    match stats:
        case "wiek":
            _sharedViews.ageGraphs(all_ages, AgesButDictionary, term_number)
        case "edukacja":
            EducationDictionary = get_committee_member_details(
                clubsButBetter, term_number, 'edukacja')
            _sharedViews.MoreStats(EducationDictionary)
        case "profesja":
            ProfessionDictionary = get_committee_member_details(
                clubsButBetter, term_number, 'profesja')
            _sharedViews.MoreStats(ProfessionDictionary)
        case "brak":
            st.write("")
