import streamlit as st
#from streamlit_push_notifications import send_push
from Controller.current_number import get_term_number, get_sitting_number, get_voting_number
from api_wrappers.interpelation import get_interpelation, get_title, get_replies
import time

st.title("System Powiadomień Sejmowych")
# @st.cache_data


def load_numbers():
    term_number = get_term_number()
    sitting_number = get_sitting_number(term_number)
    voting_number = get_voting_number(term_number, sitting_number)
    return term_number, sitting_number, voting_number

# Funkcja do sprawdzania nowych głosowań


def check_new_voting():
    term_number, sitting_number, voting_number = load_numbers()
    last_voting = st.session_state.get('last_voting', (0, 0, 0))

    if (term_number, sitting_number, voting_number) != last_voting:
        st.write(f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu")
        #send_push(
        #    title="Nowe głosowanie!",
        #    body=f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu"
        #)
        st.session_state.last_voting = (
            term_number, sitting_number, voting_number)
        return True
    return False

# Funkcja do sprawdzania odpowiedzi na interpelacje


def check_interpellation_replies(term, num):
    current_replies = get_replies(term, num)[0]
    last_replies = st.session_state.get(f'last_replies_{term}_{num}', [])

    if current_replies != last_replies:
        new_replies = [
            reply for reply in current_replies if reply not in last_replies]
        if new_replies:
            title = get_title(term, num)
            st.write(f"Otrzymano nową odpowiedź na interpelację: {title}")
            #send_push(
            #    title="Nowa odpowiedź na interpelację!",
            #    body=f"Otrzymano nową odpowiedź na interpelację: {title}"
            #)
            st.session_state[f'last_replies_{term}_{num}'] = current_replies
            return True
    return False


def loadView():
    # Inicjalizacja stanu sesji dla obserwowanych interpelacji
    if 'watched_interpellations' not in st.session_state:
        st.session_state.watched_interpellations = []

    # Interface użytkownika
    st.header("Obserwowane Interpelacje")
    term = st.number_input("Numer Kadencji", value=10,
                           min_value=1, key='input_1')
    interpellation_num = st.number_input(
        "Numer Interpelacji", value=1, min_value=1)

    if st.button("Dodaj do obserwowanych"):
        new_interpellation = (term, interpellation_num)
        if new_interpellation not in st.session_state.watched_interpellations:
            st.session_state.watched_interpellations.append(new_interpellation)
            st.success(
                f"Dodano interpelację {interpellation_num} z kadencji {term} do obserwowanych.")
        else:
            st.warning("Ta interpelacja jest już obserwowana.")

    st.subheader("Lista obserwowanych interpelacji:")
    for t, num in st.session_state.watched_interpellations:
        st.write(f"Kadencja {t}, Interpelacja {num}")
        if st.button(f"Usuń {t}-{num}"):
            st.session_state.watched_interpellations.remove((t, num))
            st.rerun()

    # Przycisk do manualnego sprawdzenia aktualizacji
    if st.button("Sprawdź aktualizacje interpelacji"):
        with st.spinner("Sprawdzanie nowych głosowań i odpowiedzi na interpelacje..."):
            new_replies = any(check_interpellation_replies(t, num)
                              for t, num in st.session_state.watched_interpellations)

            if new_replies:
                st.success(
                    "Znaleziono nowe aktualizacje! Sprawdź powiadomienia.")
            else:
                st.info("Brak nowych aktualizacji.")

    # Przycisk do manualnego sprawdzenia aktualizacji
    if st.button("Sprawdź aktualizacje głosowań"):
        with st.spinner("Sprawdzanie nowych głosowań i odpowiedzi na interpelacje..."):
            new_voting = check_new_voting()
            if new_voting:
                st.success(
                    "Znaleziono nowe aktualizacje! Sprawdź powiadomienia.")
            else:
                st.info("Brak nowych aktualizacji.")

    # Automatyczne sprawdzanie co jakiś czas (np. co 5 minut)
    if st.checkbox("Włącz automatyczne sprawdzanie interpelacji"):
        update_interval = st.slider(
            "Częstotliwość sprawdzania (w minutach)", 1, 60, 5)
        st.write(f"Automatyczne sprawdzanie co {update_interval} minut.")

        placeholder = st.empty()
        while True:
            with placeholder.container():
                new_replies = any(check_interpellation_replies(t, num)
                                  for t, num in st.session_state.watched_interpellations)

                if new_replies:
                    st.success(
                        "Znaleziono nowe aktualizacje! Sprawdź powiadomienia.")
                else:
                    st.info("Brak nowych aktualizacji.")

                latest_check = time.strftime("%Y-%m-%d %H:%M:%S")
                st.write(f"Ostatnie sprawdzenie: {latest_check}")

            time.sleep(update_interval * 60)

    # Automatyczne sprawdzanie co jakiś czas (np. co 5 minut)
    if st.checkbox("Włącz automatyczne sprawdzanie głosowań"):
        update_interval = st.slider(
            "Częstotliwość sprawdzania (w minutach)", 1, 60, 5)
        st.write(f"Automatyczne sprawdzanie co {update_interval} minut.")

        placeholder = st.empty()
        while True:
            with placeholder.container():
                new_voting = check_new_voting()
                if new_voting:
                    st.success(
                        "Znaleziono nowe aktualizacje! Sprawdź powiadomienia.")
                else:
                    st.info("Brak nowych aktualizacji.")

                latest_check = time.strftime("%Y-%m-%d %H:%M:%S")
                st.write(f"Ostatnie sprawdzenie: {latest_check}")

            time.sleep(update_interval * 60)


# st.sidebar.title("Informacje")
# st.sidebar.info("Ta aplikacja pozwala śledzić nowe głosowania w Sejmie oraz odpowiedzi na wybrane interpelacje.")
