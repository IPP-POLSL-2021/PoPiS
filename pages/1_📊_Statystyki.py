import streamlit as st
from View import statystykiKomisji, statystykiPoslow

st.set_page_config(page_title="Statystyki", page_icon="📊", layout="wide")
#st.title("📊 Statystyki")

tab1, tab2 = st.tabs(["Komisje", "Posłowie"])

with tab1:
    st.header("Komisje - Statystyki")
    statystykiKomisji.loadView()

with tab2:
    st.header("Posłowie - Statystyki")
    statystykiPoslow.loadView()