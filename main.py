import streamlit as st
import asyncio
from View import correlation, statystykiKomisji, BasicStats, calculator, coalition_viewer, view_vote, watch_interpelation, komisje, kalkulator, benford_view

st.sidebar.title("Nawigacja")


def ViewSelection():

    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Obserwuj Interpelacje", "Komisje - Posiedzenia", "Korelacje", 
                          "Komisje - Statystyki", "Posłowie - Statystyki", "kalkulator", 
                          "kalkulator wersja 2", "koalicje", "glosowania", "Rozkład Benforda"])

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
        case "kalkulator":
            calculator.loadView()
        case "kalkulator wersja 2":
            kalkulator.loadView()
        case "koalicje":
            coalition_viewer.loadView()
        case "glosowania":
            view_vote.loadView()
        case "Rozkład Benforda":
            benford_view.loadView()


ViewSelection()
