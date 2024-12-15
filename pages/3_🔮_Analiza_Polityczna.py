import streamlit as st
from View import coalition_viewer, calculator, correlation, benford_view
# st.title("🔮 Analiza Polityczna")
st.set_page_config(page_title="Analiza Polityczna",
                   page_icon="🔮", layout="wide")
tab1, tab2, tab3, tab4 = st.tabs(
    ["Potencjalne Koalicje", "Kalkulator Wyborczy", "Korelacje Wyborcze", "Prawo Benforda"])

with tab1:
    st.header("Potencjalne Koalicje")
    coalition_viewer.loadView()

with tab2:
    st.header("Kalkulator Wyborczy")
    calculator.loadView()
with tab3:
    st.header("Korelacje")
    correlation.loadView()
with tab4:
    st.header("Rozkład Benforda")
    benford_view.loadView()
