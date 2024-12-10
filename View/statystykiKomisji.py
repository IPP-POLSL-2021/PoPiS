from api_wrappers.committees import get_committee_stats, get_committees, get_committee_member_ages, get_committee_member_details
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from View import _sharedViews
from st_aggrid import AgGrid


def loadView():
    # Create columns for input fields
    col1, col2 = st.columns(2)
    with col1:
        term_number = st.number_input(
            "Kadencja sejmu", min_value=3, value=10, key='term_input_stats')
    with col2:
        codes = ["Wybierz komisje"]
        codes.extend(
            [f"{committee['name']} - {committee['code']}" for committee in get_committees(term_number)])
        codes.append("łącznie")
        selectedCommittee = st.selectbox(
            "Komisja, której statystyki cię interesują",
            options=list(codes),
            key='committee_select_stats'
        )

    if selectedCommittee == "Wybierz komisje":
        st.info("Wybierz komisję aby zobaczyć statystyki")
        return

    # Create tabs for different views
    overview_tab, details_tab = st.tabs(
        ["Przegląd Komisji", "Statystyki Szczegółowe"])

    if selectedCommittee != "łącznie":
        selectedCommittee = selectedCommittee.split("-")[-1][1:]

    committee_stats = get_committee_stats(term_number, selectedCommittee)
    clubs = pd.DataFrame.from_dict(committee_stats['clubs'], orient='index')
    MPs = pd.DataFrame.from_dict(committee_stats['members'], orient='index')
    clubsButBetter = committee_stats['clubs']

    with overview_tab:
        # Create columns for overview data
        chart_col, data_col = st.columns([2, 1])

        with chart_col:
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
                labels={'Partie': 'Partie',
                        'Liczba członków': 'Liczba członków'}
            )
            fig.update_layout(
                xaxis_title='Partie',
                yaxis_title='Liczba członków',
                title_font_size=16,
                xaxis_tickangle=45
            )
            st.plotly_chart(fig)

        with data_col:
            # Clean column names
            clubs.columns = [str(col).replace('.', '_')
                             for col in clubs.columns]
            AgGrid(clubs)

        # Display MPs data if "łącznie" is selected
        if selectedCommittee == "łącznie":
            st.subheader("Dane wszystkich posłów")
            st.dataframe(MPs, use_container_width=True)

    with details_tab:
        # Age and other statistics

        # Statistics selection
        stats = st.selectbox(
            "Wybierz statystykę",
            ["Wybierz typ statystyki", "wiek", "edukacja", "profesja"],
            key='stats_select'
        )

        if stats == "Wybierz typ statystyki":
            st.info("Wybierz typ statystyki aby zobaczyć szczegółowe dane")
        else:
            match stats:
                case "wiek":
                    DataframeAges, AgesButDictionary = get_committee_member_ages(
                        clubsButBetter, term_number)
                    all_ages = DataframeAges.values.flatten()
                    all_ages = pd.Series(all_ages).dropna()
                    _sharedViews.ageGraphs(
                        all_ages, AgesButDictionary, term_number)
                case "edukacja":
                    EducationDictionary = get_committee_member_details(
                        clubsButBetter, term_number, 'edukacja')
                    _sharedViews.MoreStats(EducationDictionary)
                case "profesja":
                    ProfessionDictionary = get_committee_member_details(
                        clubsButBetter, term_number, 'profesja')
                    _sharedViews.MoreStats(ProfessionDictionary)
