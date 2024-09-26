import requests
from streamlit_push_notifications import send_push
from datetime import datetime, date
import streamlit as st

def get_ten_acts_this_year():
    thisYear = datetime.now().year
    var = 1400
    while (True):
        response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}/{var}")
        if response.status_code != 200:
            print(var-1)
            listOfActs = []
            for iter in range(1, 11):
                response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}/{var-1}")
                listOfActs.append(response.json())
                var=var-1
            return listOfActs
        else:
            var += 1

def did_today_new_ustawa_obowiazuje():
    thisYear = datetime.now().year
    today = datetime.date(datetime.now())
    var = 1400
    while (True):
        response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}/{var}")
        if response.status_code != 200:
            response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}/{var - 1}")
            resjson = response.json()
            if 'changeDate' in resjson:
                if (date.fromisoformat(resjson['changeDate'][0:10])==today):
                    return True
                else:
                    return False
        else:
            var += 1


def get_titles_of_record(records):
    list_titles = []
    for i in records:
        if 'title' in i:
            list_titles.append(f"{i['type']}: {i['title']}")
        else:
            print("Blad, brak tytulu")
        
    return list_titles


import pdfplumber
import PyPDF2
import re
from bs4 import BeautifulSoup
from sentimentpl.models import SentimentPLModel

def analiza_stenogramow():  

    

    def fetch_pdf_link(html_file):
        # Otwórz lokalny plik HTML
        with open(html_file, 'r', encoding='utf-8') as file:
            page_content = file.read()

        # Parsowanie HTML za pomocą BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')

        # Znalezienie pierwszego linku do pliku PDF (zgodnie z selektorem CSS)
        selector = '#view\\:_id1\\:_id2\\:facetMain\\:rContent\\:0\\:_id136\\:0\\:_id138'
        stenogram_link = soup.select_one(selector)

        if stenogram_link:
            return stenogram_link['href']
        else:
            raise ValueError("Nie znaleziono linku do PDF w podanym pliku HTML.")

    # 2. Pobieranie pliku PDF z podanego linku
    def download_pdf(pdf_url, output_path='stenogram.pdf'):
        # Pobieranie pliku PDF z URL
        response = requests.get(pdf_url)

        if response.status_code == 200:
            # Zapisz plik PDF lokalnie
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"Plik PDF został pobrany i zapisany jako {output_path}")
        else:
            raise Exception(f"Błąd podczas pobierania pliku PDF: {response.status_code}")

    # Główna funkcja, która pobiera link i zapisuje plik PDF
    def main():
        html_file = 'C:\\Users\\HP\\Documents\\GitHub\\PoPiS\\Data\\Sprawozdania stenograficzne z posiedzeń Sejmu - Sejm Rzeczypospolitej Polskiej.html'

        try:
            # Znajdź link do pliku PDF w pliku HTmL
            pdf_url = fetch_pdf_link(html_file)
            print(f"Link do pliku PDF: {pdf_url}")

            # Pobierz plik PDF
            download_pdf(pdf_url)

        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    
   

    sentiment_analyzer_pl = SentimentPLModel(from_pretrained='latest')










def loadView():
    analiza_stenogramow()
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

    tenRecords=get_ten_acts_this_year()
    titlesOfRecords = get_titles_of_record(tenRecords)
    print(titlesOfRecords)

    st.title("Lista ostatnich 10 obowiązujących aktów prawnych")

    for title in titlesOfRecords:
        st.write(title)