import streamlit as st
import asyncio
from View import test

from View import test2, statystykiKomisji
st.sidebar.title("Nawigacja")


def ViewSelection():

    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Aplikacja 1", "Aplikacja 2", "statystyki"])

    # t1 = threading.Thread(target=discordBotStart, name='t1')
    match page:
        case "Aplikacja 1":
            test.loadView()
        case "Aplikacja 2":
            test2.loadView()
        case "statystyki":
            statystykiKomisji.loadView()
    # if page == "Aplikacja 1":

    #     test.loadView()
    # elif page == "Aplikacja 2":

    #     test2.loadView()


ViewSelection()
