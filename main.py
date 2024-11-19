import streamlit as st
import asyncio
from View import correlation, statystykiKomisji, BasicStats, calculator, coalition_viewer, wyboryKalkulator, view_vote, watch_interpelation, komisje, test3, benford_view

st.sidebar.title("Nawigacja")


def ViewSelection():

    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Obserwuj Interpelacje", "Komisje - Posiedzenia", "Korelacje",
                           "Komisje - Statystyki", "Posłowie - Statystyki", "kalkulator", "ustawy",
                           "koalicje", "glosowania", "kalkulator wyników wyborów", "Rozkład Benforda"])

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
        case "ustawy":
            test3.loadView()
        case "koalicje":
            coalition_viewer.loadView()
        case "glosowania":
            view_vote.loadView()
        case "kalkulator wyników wyborów":
            wyboryKalkulator.loadView()
        case "Rozkład Benforda":
            benford_view.loadView()


ViewSelection()
