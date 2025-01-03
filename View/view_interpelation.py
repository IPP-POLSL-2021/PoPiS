import streamlit as st
from api_wrappers.interpelation import get_interpelation, get_title, get_replies, get_authors, get_date, get_receipent
import requests


def loadView():
    st.markdown(
        "<style>.st-emotion-cache-wprd1t{overflow: hidden;}</style>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        term = st.number_input("Numer Kadencji", value=10,
                               min_value=1, key='term_input')
    with col2:
        interpellation_num = st.number_input(
            "Numer Interpelacji", value=1, min_value=1, key='interpellation_input')
    response = get_interpelation(term, interpellation_num)
    st.write(get_title(response=response))
    adresaci = get_receipent(response=response)
    #  jest też taka opcja {', '.join(adresaci)}
    if len(adresaci) > 1:
        st.write(
            f"Wysłana {get_date(mode=0,response=response)} i dnia {get_date(mode=1, response=response)} skierowana do")
        # st.write("Adresaci interpelacji:")
        for adr in adresaci:
            st.write(adr)
    else:
        st.write(
            f"Wysłana {get_date(mode=0,response=response)} i dnia {get_date(mode=1, response=response)} skierowana do {adresaci[0]}")
    # st.write(
    #    f"Wysłana {get_date(mode=0,response=response)} i dnia {get_date(mode=1, response=response)} skierowana do {str(get_receipent(response=response))[2:-2]}")
    st.write("Autorzy interpelacji:")
    col1, col2 = st.columns([1, 5])
    for author in get_authors(response=response):
        with col1:
            with st.container(height=175, border=False):
                st.image(author[2])
        with col2:
            with st.container(height=175, border=False):

                st.write(f"{author[0]}, {author[3]} z klubu {author[1]}")

        # st.image
    # st.write("Odpowiedzi na interpelację:")
    # Chyba wszystko co jest tutaj jest już w tym drugim?
    # for reply in current_replies[0]:
    # st.link_button("Zobacz pdf", reply)
    current_replies = get_replies(term, interpellation_num, response=response)
    for reply in current_replies[1]:
        st.html(requests.get(reply).content.decode('utf-8'))
