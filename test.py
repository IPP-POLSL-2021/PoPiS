import streamlit as st
from streamlit_push_notifications import send_push
from Votes.current_number import get_term_number, get_sitting_number, get_voting_number
from Interpelations.get_answer import get_interpelation
#from datetime import date
# date.today()
#from dotenv import load_dotenv
import os
st.title("Popis")

@st.cache_data
def load_numbers():
    #load_dotenv()
    term_number = get_term_number()
    sitting_number = get_sitting_number(term_number)
    voting_number = get_voting_number(term_number, sitting_number)
    return term_number,sitting_number,voting_number

st.header("Interpelacje")
term_number = st.number_input(
    "Numer Kadencji", value=10, placeholder="Wpisz numer"
)
#interpelation_number = st.number_input(
#    "Numer Interpelacji", value=None, placeholder="Wpisz numer"
#)
interpelation_number = 3999
interpelation = get_interpelation(term_number,str(interpelation_number))
# Posłów zwraca jako numer a nie imię i nazwisko (literalnie rok 1914)
# To na później
# relative_date = date.today() - interpelation.receipt_date
# Adresatów może być wiele ofc todo
#st.markdown(f"{interpelation.title} wysłana przez {interpelation.from_} skierowana do {interpelation.to[0]}")
#st.markdown("%i wysłana przez %i skierowana do %i" % ("interpelation.title", "interpelation.from_","interpelation.to"))
            
#st.json
# st.html
#send_push(title=interpelation.title, body=f"Wysłana przez {interpelation.from_} {date.today() - interpelation.sent_date} dni temu")
st.header("Głosowania")
if st.button("Pokaż najnowsze dane"):
    term_number,sitting_number,voting_number=load_numbers()
    send_push(title="Najnowsze głosowanie to",
              body=f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu")
             
st.title("Jak się kliknie raz o powiadomienie to drugi raz już nie wyjdzie póki się nie wyśle innego powiadomienia")              
if st.button("Reset"):
    send_push(title="Test", body=f"Body")
