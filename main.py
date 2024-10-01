
import streamlit as st
import asyncio
from View import test

from Controller.telegrambot import start_telegram_bot
from View import test2
st.sidebar.title("Nawigacja")


def ViewSelection():

    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Aplikacja 1", "Aplikacja 2"])

    # t1 = threading.Thread(target=discordBotStart, name='t1')
    if page == "Aplikacja 1":

        test.loadView()
    elif page == "Aplikacja 2":

        test2.loadView()


ViewSelection()
# try:
#     start_telegram_bot()
# except Exception as e:
#     print(f"chyba już działa nwm masz tu błąd i naparw{e}")
