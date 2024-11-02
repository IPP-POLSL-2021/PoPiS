import streamlit as st
from Controller import MPsStats


def loadView():
    st.markdown("hwilowo nic")
    MPsStats.groupMpsByClub(10)
