import streamlit as st
from View import view_interpelation, ustawy, komisje, view_vote

st.title("🗳️ Procesy Parlamentarne")

tab1, tab2, tab3, tab4 = st.tabs(["Interpelacje", "Ustawy", "Komisje", "Głosowania Posłów"])

with tab1:
    st.header("Interpelacje")
    view_interpelation.loadView()

with tab2:
    st.header("Ustawy")
    ustawy.loadView()

with tab3:
    st.header("Komisje")
    komisje.loadView()

with tab4:
    st.header("Głosowania Posłów")
    view_vote.loadView()