import requests
from streamlit_push_notifications import send_push
from datetime import datetime, date
import streamlit as st
from sentimentpl.models import SentimentPLModel
from Controller.acts import get_all_acts_this_year, get_titles_of_record,did_today_new_ustawa_obowiazuje,  get_process_details, get_legislative_processes


BASE_URL = "https://api.sejm.gov.pl"
TERM = 10  # Przykładowy termin Sejmu

model = SentimentPLModel(from_pretrained='latest')

def get_proceedings(term):
    response = requests.get(f"{BASE_URL}/sejm/term{term}/proceedings", headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Nie udało się pobrać listy posiedzeń. Kod błędu: {response.status_code}")
        return []

def get_proceeding_details(term, proceeding_number):
    response = requests.get(f"{BASE_URL}/sejm/term{term}/proceedings/{proceeding_number}", headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Nie udało się pobrać szczegółów posiedzenia. Kod błędu: {response.status_code}")
        return {}

def get_transcripts(term, proceeding_number, date, transcript_number=0):
    header = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Referer': BASE_URL
    }
    response = requests.get(
        f"{BASE_URL}/sejm/term{term}/proceedings/{proceeding_number}/{date}/transcripts/{transcript_number}",
        headers=header
    )
    
    
    if response.status_code == 200:
        return response.json().get('statements', [])
    else:
        st.error(f"Nie udało się pobrać transkryptów wypowiedzi. Kod błędu: {response.status_code}")
        return []

def analyze_sentiment(statements):
    sentiment_results = defaultdict(lambda: {'positive': 0, 'neutral': 0, 'negative': 0, 'total': 0})

    for statement in statements:
        text = statement.get('content', "")
        author = statement.get('author', "Nieznany")
        score = model(text).item()  # Zakres wyniku: od -1 (negatywny) do 1 (pozytywny)

        if score > 0.3:
            sentiment_results[author]['positive'] += 1
        elif score < -0.3:
            sentiment_results[author]['negative'] += 1
        else:
            sentiment_results[author]['neutral'] += 1

        sentiment_results[author]['total'] += 1

    for author, counts in sentiment_results.items():
        total = counts['total']
        counts['positive'] = round((counts['positive'] / total) * 100, 2)
        counts['neutral'] = round((counts['neutral'] / total) * 100, 2)
        counts['negative'] = round((counts['negative'] / total) * 100, 2)

    return sentiment_results

def loadView():
    
    st.title("Analiza sentymentu wypowiedzi posłów")

    proceedings = get_proceedings(TERM)
    if proceedings:
        proceeding_options = [f"{p['number']}" for p in proceedings]
        selected_proceeding = st.selectbox("Wybierz numer posiedzenia Sejmu", proceeding_options)
        
        proceeding_details = get_proceeding_details(TERM, selected_proceeding)
        dates = proceeding_details.get('dates', [])
        
        if dates:
            selected_date = st.selectbox("Wybierz datę posiedzenia", dates)
            
            statements = get_transcripts(TERM, selected_proceeding, selected_date)
            
            if statements:
                st.write(f"**Liczba wypowiedzi pobranych z API:** {len(statements)}")
                sentiment_results = analyze_sentiment(statements)

                st.subheader("Wyniki analizy sentymentu wypowiedzi posłów")
                for author, sentiments in sentiment_results.items():
                    st.write(f"**Poseł:** {author}")
                    st.write(f"Pozytywne: {sentiments['positive']}%")
                    st.write(f"Neutralne: {sentiments['neutral']}%")
                    st.write(f"Negatywne: {sentiments['negative']}%")
                    st.write("---")
            else:
                st.write("Brak wypowiedzi dla wybranej daty posiedzenia.")
        else:
            st.write("Brak dostępnych dat dla wybranego posiedzenia.")
    else:
        st.write("Brak dostępnych posiedzeń.")



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
    