import streamlit as st
from streamlit_push_notifications import send_push
from current_number import get_term_number, get_sitting_number, get_voting_number
#from dotenv import load_dotenv
import os
st.title("Powiadomienie o głosowaniu")

@st.cache_data
def load_numbers():
    #load_dotenv()
    term_number = get_term_number()
    sitting_number = get_sitting_number(term_number)
    voting_number = get_voting_number(term_number, sitting_number)
    return term_number,sitting_number,voting_number

term_number,sitting_number,voting_number=load_numbers()

if st.button("Pokaż najnowsze dane"):
    send_push(title="Najnowsze głosowanie to",
              body=f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu")
             
st.title("Jak się kliknie raz o powiadomienie to drugi raz już nie wyjdzie póki się nie wyśle innego powiadomienia")              
if st.button("Reset"):
    send_push(title="Test", body=f"Body")
