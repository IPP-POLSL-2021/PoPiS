import streamlit as st
from View import correlation, watch_interpelation, benford_view

st.title("🚧 W budowie")

tab1, tab2, tab3 = st.tabs(["Korelacje", "Obserwuj Interpelacje", "Rozkład Benforda"])

with tab1:
    st.header("Korelacje")
    correlation.loadView()

with tab2:
    st.header("Obserwuj Interpelacje")
    watch_interpelation.loadView()

with tab3:
    st.header("Rozkład Benforda")
    benford_view.loadView()