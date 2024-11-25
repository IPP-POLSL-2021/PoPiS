import streamlit as st
from Controller.current_number import get_term_number, get_sitting_number, get_voting_number
from api_wrappers.interpelation import get_interpelation, get_title, get_replies
import time

def load_numbers():
    term_number = get_term_number()
    sitting_number = get_sitting_number(term_number)
    voting_number = get_voting_number(term_number, sitting_number)
    if voting_number == 0:
        sitting_number = sitting_number-1
        voting_number = get_voting_number(term_number,sitting_number)
    return term_number, sitting_number, voting_number

def check_new_voting():
    term_number, sitting_number, voting_number = load_numbers()
    last_voting = st.session_state.get('last_voting', (0, 0, 0))
    if voting_number==0:
        sitting_number=sitting_number-1
        voting_number=get_voting_number(sitting=sitting_number)
    if (term_number, sitting_number, voting_number) != last_voting:
        st.write(f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu")
        st.session_state.last_voting = (term_number, sitting_number, voting_number)
        return True
    return False

def check_interpellation_replies(term, num):
    current_replies = get_replies(term, num)[0]
    last_replies = st.session_state.get(f'last_replies_{term}_{num}', [])

    if current_replies != last_replies:
        new_replies = [reply for reply in current_replies if reply not in last_replies]
        if new_replies:
            title = get_title(term, num)
            st.write(f"Otrzymano nową odpowiedź na interpelację: {title}")
            st.session_state[f'last_replies_{term}_{num}'] = current_replies
            return True
    return False

def loadView():
    #st.title("System Powiadomień Sejmowych")
    st.header("Obserwowane Interpelacje")
    
    # Inicjalizacja stanu sesji dla obserwowanych interpelacji
    if 'watched_interpellations' not in st.session_state:
        st.session_state.watched_interpellations = []

    # Interface użytkownika
    col1, col2 = st.columns(2)
    with col1:
        term = st.number_input("Numer Kadencji", value=10, min_value=1, key='term_input')
    with col2:
        interpellation_num = st.number_input("Numer Interpelacji", value=1, min_value=1, key='interpellation_input')

    if st.button("Dodaj do obserwowanych", key='add_button'):
        new_interpellation = (term, interpellation_num)
        if new_interpellation not in st.session_state.watched_interpellations:
            st.session_state.watched_interpellations.append(new_interpellation)
            st.success(f"Dodano interpelację {interpellation_num} z kadencji {term} do obserwowanych.")
        else:
            st.warning("Ta interpelacja jest już obserwowana.")

    st.subheader("Lista obserwowanych interpelacji:")
    for idx, (t, num) in enumerate(st.session_state.watched_interpellations):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"Kadencja {t}, Interpelacja {num}")
        with col2:
            if st.button(f"Usuń", key=f'remove_{idx}'):
                st.session_state.watched_interpellations.remove((t, num))
                st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sprawdź aktualizacje interpelacji", key='check_interpellations'):
            with st.spinner("Sprawdzanie odpowiedzi na interpelacje..."):
                new_replies = any(check_interpellation_replies(t, num)
                                for t, num in st.session_state.watched_interpellations)
                if new_replies:
                    st.success("Znaleziono nowe aktualizacje!")
                else:
                    st.info("Brak nowych aktualizacji.")

    with col2:
        if st.button("Sprawdź aktualizacje głosowań", key='check_votings'):
            with st.spinner("Sprawdzanie nowych głosowań..."):
                new_voting = check_new_voting()
                if new_voting:
                    st.success("Znaleziono nowe głosowania!")
                else:
                    st.info("Brak nowych głosowań.")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("Włącz automatyczne sprawdzanie interpelacji", key='auto_check_interpellations'):
            update_interval = st.slider(
                "Częstotliwość sprawdzania interpelacji (minuty)", 
                1, 60, 5, 
                key='interval_interpellations'
            )
            st.write(f"Automatyczne sprawdzanie co {update_interval} minut.")

            placeholder = st.empty()
            while True:
                with placeholder.container():
                    new_replies = any(check_interpellation_replies(t, num)
                                    for t, num in st.session_state.watched_interpellations)
                    if new_replies:
                        st.success("Znaleziono nowe aktualizacje!")
                    else:
                        st.info("Brak nowych aktualizacji.")
                    st.write(f"Ostatnie sprawdzenie: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(update_interval * 60)

    with col2:
        if st.checkbox("Włącz automatyczne sprawdzanie głosowań", key='auto_check_votings'):
            update_interval = st.slider(
                "Częstotliwość sprawdzania głosowań (minuty)", 
                1, 60, 5,
                key='interval_votings'
            )
            st.write(f"Automatyczne sprawdzanie co {update_interval} minut.")

            placeholder = st.empty()
            while True:
                with placeholder.container():
                    new_voting = check_new_voting()
                    if new_voting:
                        st.success("Znaleziono nowe głosowania!")
                    else:
                        st.info("Brak nowych głosowań.")
                    st.write(f"Ostatnie sprawdzenie: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(update_interval * 60)
