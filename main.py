import streamlit as st
import threading
from View import test
import asyncio
from Controller.dicordBot import run
from View import test2
st.sidebar.title("Nawigacja")


def ViewSelection():
    page = st.sidebar.selectbox(
        "Wybierz stronę", ["Aplikacja 1", "Aplikacja 2"])

    if page == "Aplikacja 1":
        test.loadView()
    elif page == "Aplikacja 2":
        test2.loadView()


ViewSelection()
t1 = threading.Thread(target=run, name='t1')
t1.daemon = "false"
t1.start()
