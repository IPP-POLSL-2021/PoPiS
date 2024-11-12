import streamlit as st
import asyncio
from View import test, test2, statystykiKomisji, BasicStats, calculator, coalition_viewer, view_vote
st.sidebar.title("Nawigacja")


def ViewSelection():

    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Aplikacja 1", "Aplikacja 2", "statystyki", "statystyki ogólne", "kalkuator", "koalicje", "glosowania"])

    # t1 = threading.Thread(target=discordBotStart, name='t1')
    match page:
        case "Aplikacja 1":
            test.loadView()
        case "Aplikacja 2":
            test2.loadView()
        case "statystyki":
            statystykiKomisji.loadView()
        case "statystyki ogólne":
            BasicStats.loadView()
        case "kalkuator":
            calculator.loadView()
        case "koalicje":
            coalition_viewer.loadView()
        case "glosowania":
            view_vote.loadView()

            # if page == "Aplikacja 1":

            #     test.loadView()
            # elif page == "Aplikacja 2":

            #     test2.loadView()


ViewSelection()
