import streamlit as st
from Controller import MPsStats


def loadView():
    st.markdown("hwilowo nic")
    MpGroupedList, MpsList, MpNamesByClub = MPsStats.groupMpsByClub(10)
    MPsStats.ageStats(10, MpGroupedList, MpsList)
