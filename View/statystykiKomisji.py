from Controller.Committees import CommitteeStats, CommitteesList, CommitteeAge, CommitteeEducation
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

    codes = [committee['code'] for committee in CommitteesList(term_number)]
    codes.append("łącznie")
    selectedCommittee = st.selectbox(
        "komisja której statystyki cię interesują (niektóre dostępne tylko dla obecnej kadencji)", options=list(codes)
    )

    clubs, MPs, clubsButBetter = CommitteeStats(term_number, selectedCommittee)
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
    #st.dataframe(clubs, use_container_width=True)
    #if selectedCommittee == "łącznie":
    #    MPs.columns = [str(col).replace('.', '_') for col in MPs.columns]
    #    AgGrid(MPs)
    if selectedCommittee == "łącznie":
        st.dataframe(MPs, use_container_width=True)

    DataframeAges, AgesButDictionary = CommitteeAge(clubsButBetter, term_number)
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
            EducationDictionary = CommitteeEducation(clubsButBetter, term_number, stats)
            _sharedViews.MoreStats(EducationDictionary)
        case "profesja":
            EducationDictionary = CommitteeEducation(clubsButBetter, term_number, stats)
            _sharedViews.MoreStats(EducationDictionary)
        case "brak":
            st.write("")
