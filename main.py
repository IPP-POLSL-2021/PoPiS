import streamlit as st
import asyncio
from View import correlation, statystykiKomisji, BasicStats, calculator, coalition_viewer, view_vote, watch_interpelation, komisje

st.sidebar.title("Nawigacja")


def ViewSelection():

    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Obserwuj Interpelacje", "Komisje - Posiedzenia", "Korelacje", "Komisje - Statystyki", "Posłowie - Statystyki", "kalkulator", "koalicje", "glosowania"])

    # t1 = threading.Thread(target=discordBotStart, name='t1')
    match page:
        case "Obserwuj Interpelacje":
            watch_interpelation.loadView()
        case "Komisje - Posiedzenia":
            komisje.loadView()
        case "Korelacje":
            correlation.loadView()
        case "Komisje - Statystyki":
            statystykiKomisji.loadView()
        case "Posłowie - Statystyki":
            BasicStats.loadView()
        case "kalkuator":
            calculator.loadView()
        case "koalicje":
            coalition_viewer.loadView()
        case "glosowania":
            view_vote.loadView()

ViewSelection()
