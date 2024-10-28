import requests
from streamlit_push_notifications import send_push
from datetime import datetime, date
import streamlit as st
from sentimentpl.models import SentimentPLModel
from Controller.acts import get_all_acts_this_year, get_titles_of_record,did_today_new_ustawa_obowiazuje,  get_process_details, get_legislative_processes
import pdfplumber
from io import BytesIO
import re
from collections import defaultdict

BASE_URL = "https://api.sejm.gov.pl"
TERM = 10  # Przykładowy termin Sejmu

model = SentimentPLModel(from_pretrained='latest')

def get_proceedings(term):
    response = requests.get(f"{BASE_URL}/sejm/term{term}/proceedings")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Nie udało się pobrać listy posiedzeń. Kod błędu: {response.status_code}")
        return []

def get_proceeding_details(term, proceeding_number):
    response = requests.get(f"{BASE_URL}/sejm/term{term}/proceedings/{proceeding_number}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Nie udało się pobrać szczegółów posiedzenia. Kod błędu: {response.status_code}")
        return {}

def get_transcript(term, proceeding_number, date, transcript_number=0):

    response = requests.get(
        f"{BASE_URL}/sejm/term{term}/proceedings/{proceeding_number}/{date}/transcripts/pdf"
    )
    
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        st.error(f"Nie udało się pobrać pliku PDF. Kod błędu: {response.status_code}")
        return None

def extract_text_from_pdf_without_parentheses(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            # Usuwamy tekst w nawiasach za pomocą regexu
            page_text = re.sub(r'\(.*?\)', '', page_text)
            text += page_text + "\n"
    return text

    

def loadView():
    st.title("Analiza sentymentu wypowiedzi posłów z transkryptu")

    proceeding_number = get_proceedings(TERM)
    if proceeding_number:
        proceeding_options = [f"{p['number']}" for p in proceeding_number]
        selected_proceeding = st.selectbox("Wybierz numer posiedzenia Sejmu", proceeding_options)
        
        proceeding_details = get_proceeding_details(TERM, selected_proceeding)
        date = proceeding_details.get('dates', [])
        
        if date:
            selected_date = st.selectbox("Wybierz datę posiedzenia", date)

    if st.button("Pobierz i analizuj transkrypt"):
        
        pdf_file = get_transcript(TERM, proceeding_number, date)
        if pdf_file:
            text = extract_text_from_pdf_without_parentheses(pdf_file)
            st.subheader("Przykładowy tekst bez nawiasów")
            st.write(text[:1000]) 

            
            
    
    


    st.title("Śledzenie Procesu Legislacyjnego")

    processes = get_legislative_processes(TERM)

    if processes:
        process_titles = [f"{p['number']} - {p['title']}" for p in processes]
        selected_process = st.selectbox("Wybierz proces legislacyjny", process_titles)
        
        selected_process_number = selected_process.split(" - ")[0]

        process_details = get_process_details(TERM, selected_process_number)
        
        if process_details:
            st.subheader("Szczegóły procesu legislacyjnego")
            st.write(f"**Tytuł:** {process_details.get('title', 'Brak tytułu')}")
            st.write(f"**Opis:** {process_details.get('description', 'Brak opisu')}")
            st.write(f"**Data rozpoczęcia:** {process_details.get('processStartDate', 'Brak daty')}")
            

            stages = process_details.get('stages', [])
            if stages:
                st.subheader("Etapy procesu")
                for stage in stages:
                    
                    st.write(f"**Etap:** {stage['stageName']}")
                    
                    try:
                        st.write(f"**Data:** {stage['dates']}")
                    except:
                        print("no date")
                    try:
                        st.write(f"**Decyzja:** {stage['decision']}")
                    except:
                        print("no decision")
                    st.write("---")
                    temp = stage

            else:
                st.write("Brak dostępnych etapów.")
    else:
        st.write("Brak dostępnych procesów legislacyjnych.")


    if st.button("Był dziś nowy akt prawny?"):
        if did_today_new_ustawa_obowiazuje():
            send_push(
                    title="Tak!",
                    body=f"Dodano dzisiaj nowy akt prawny"
                )
        else:
            send_push(
                    title="Nie...",
                    body=f"Nie dodano dzisiaj żadnego aktu prawnego"
                )


    acts=get_all_acts_this_year()
    if acts:
        # Przetwarzamy rekordy
        result=get_titles_of_record(acts)
        

        st.subheader("Ustawy")
        st.table([{"Tytuł ustawy": title} for title in result['ustawy']]) 

        st.subheader("Rozporządzenia")
        st.table([{"Tytuł rozporządzenia": title} for title in result['rozporzadzenia']])

    else:
        st.error("Nie udało się pobrać danych.")

       #fetch_transcripts(f"https://api.sejm.gov.pl/sejm/term10/proceedings/18/2024-09-25/transcripts/0")
    