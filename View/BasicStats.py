import streamlit as st
from Controller import MPsStats


def loadView():
    term = 10
    searchedInfo = 'edukacja'

    st.markdown("hwilowo nic")
    MpGroupedList, MpsList, MpNamesByClub = MPsStats.groupMpsByClub(10)
    MPsStats.ageStats(term, MpGroupedList, MpsList)
    MPsStats.MPsEducation(MpsList, MpGroupedList, term, searchedInfo)
