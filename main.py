import streamlit as st
from View import test, test2, test3
st.sidebar.title("Nawigacja")
page = st.sidebar.selectbox("Wybierz stronę", ["Aplikacja 1", "Aplikacja 2","Aplikacja 3"])
if page == "Aplikacja 1":
    test.loadView()
elif page == "Aplikacja 2":
    test2.loadView()
elif page == "Aplikacja 3":
    test3.loadView()
