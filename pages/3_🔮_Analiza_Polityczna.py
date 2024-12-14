import streamlit as st
from View import coalition_viewer, calculator, correlation
# st.title("🔮 Analiza Polityczna")
st.set_page_config(page_title="Analiza Polityczna",
                   page_icon="🔮", layout="wide")
tab1, tab2, tab3 = st.tabs(
    ["Potencjalne Koalicje", "Kalkulator Wyborczy", "Korelacje Wyborcze"])

with tab1:
    st.header("Potencjalne Koalicje")
    coalition_viewer.loadView()

with tab2:
    st.header("Kalkulator Wyborczy")
    calculator.loadView()
with tab3:
    st.header("Korelacje")
    correlation.loadView()
