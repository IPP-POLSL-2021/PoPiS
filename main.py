import streamlit as st
from View import test

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