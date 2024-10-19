import requests
from streamlit_push_notifications import send_push
from datetime import datetime, date
import streamlit as st
from sentimentpl.models import SentimentPLModel
from Controller.acts import get_all_acts_this_year, get_titles_of_record,did_today_new_ustawa_obowiazuje




def fetch_transcripts(url):
    
    #sitting_number = get_sitting_number(term_number)
    #response = requests.get(f"http://api.sejm.gov.pl/sejm/term10/proceedings/{sitting_number}/{data}/transcripts/0")
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
        return response.json()  # Zwróć dane w formacie JSON
    else:
        raise Exception(f"Nie udało się pobrać danych z API. Kod statusu: {response.status_code}")

def get_full_transcripts(base_url, transcript_data):
    full_transcripts = []
    
    for entry in transcript_data:
        # Jeśli wypowiedź ma dodatkowe linki (np. pod linkiem 'transcripts/001')
        if 'href' in entry:
            sub_url = f"{base_url}/{entry['href']}"
            sub_transcript = fetch_transcripts(sub_url)
            full_transcripts.append(sub_transcript)
        else:
            full_transcripts.append(entry)
    
    return full_transcripts

#def analyze_sentiment(statements):
    model = SentimentPLModel()
    results = []
    
    for statement in statements:
        person = statement.get('speaker', 'Nieznany')  # Ustal osobę wypowiadającą się
        text = statement.get('text', '')  # Pobierz tekst wypowiedzi
        sentiment = model.predict(text)  # Analiza sentymentu
        
        results.append({
            'speaker': person,
            'text': text,
            'sentiment': sentiment
        })
    
    return results
   
    sentiment_analyzer_pl = SentimentPLModel(from_pretrained='latest')


def loadView():
    
    st.title("Śledzenie Procesu Legislacyjnego")
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
    st.write(acts)
    if acts:
        # Przetwarzamy rekordy
        result=get_titles_of_record(acts)
        

        st.subheader("Ustawy")
        st.table([{"Tytuł ustawy": title} for title in result['ustawy']]) 

        st.subheader("Rozporządzenia")
        st.table([{"Tytuł rozporządzenia": title} for title in result['rozporzadzenia']])

        st.subheader("Obwieszczenia")
        st.table([{"Tytuł obwieszczenia": title} for title in result['obwieszczenia']])

    else:
        st.error("Nie udało się pobrać danych.")

       #fetch_transcripts(f"https://api.sejm.gov.pl/sejm/term10/proceedings/18/2024-09-25/transcripts/0")
    