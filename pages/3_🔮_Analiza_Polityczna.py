import streamlit as st
from View import coalition_viewer, calculator

#st.title("🔮 Analiza Polityczna")
st.set_page_config(page_title="Analiza Polityczna", page_icon="🔮", layout="wide")
tab1, tab2 = st.tabs(["Potencjalne Koalicje", "Kalkulator Wyborczy"])

with tab1:
    st.header("Potencjalne Koalicje")
    coalition_viewer.loadView()

with tab2:
    st.header("Kalkulator Wyborczy")
    calculator.loadView()