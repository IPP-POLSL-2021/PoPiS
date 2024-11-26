import streamlit as st
from View import main_page, coalition_viewer, ustawy, view_interpelation
# Ocenić przydatność, dopracować
#from View import correlation, watch_interpelation, benford_view

# Do potencjalnego złączenia razem
from View import statystykiKomisji, komisje
from View import calculator, wyboryKalkulator
from View import statystykiPoslow, view_vote
st.sidebar.title("Nawigacja")


def ViewSelection():

    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Strona Główna","Interpelacje","Komisje",
                        "Komisje - Statystyki", "Posłowie - Statystyki", "kalkulator", "ustawy",
                        "Potencjalne Koalicje", "Głosowania Posłów", "kalkulator wyników wyborów"])

    # t1 = threading.Thread(target=discordBotStart, name='t1')
    match page:
        case "Strona Główna":
            main_page.loadView()
        #case "Obserwuj Interpelacje":
        #    watch_interpelation.loadView()
        case "Interpelacje":
            view_interpelation.loadView()
        case "Komisje":
            komisje.loadView()
        #case "Korelacje":
        #    correlation.loadView()
        case "Komisje - Statystyki":
            statystykiKomisji.loadView()
        case "Posłowie - Statystyki":
            statystykiPoslow.loadView()
        case "kalkulator":
            calculator.loadView()
        case "ustawy":
            ustawy.loadView()
        case "Potencjalne Koalicje":
            coalition_viewer.loadView()
        case "Głosowania Posłów":
            view_vote.loadView()
        case "kalkulator wyników wyborów":
            wyboryKalkulator.loadView()
        #case "Rozkład Benforda":
        #    benford_view.loadView()


ViewSelection()
