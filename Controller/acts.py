import requests
from datetime import datetime, date
import streamlit as st
# Ustawienia API
BASE_URL = "https://api.sejm.gov.pl"


def get_legislative_processes(term):
    response = requests.get(f"{BASE_URL}/sejm/term{term}/processes")
    if response.status_code == 200:
        return response.json()  # Zwraca listę procesów w formacie JSON
    else:
        st.error(
            f"Nie udało się pobrać procesów legislacyjnych. Kod błędu: {response.status_code}")
        return []


def get_process_details(term, process_number):
    response = requests.get(
        f"{BASE_URL}/sejm/term{term}/processes/{process_number}")
    if response.status_code == 200:
        return response.json()  # Zwraca szczegóły procesu
    else:
        st.error(
            f"Nie udało się pobrać szczegółów procesu. Kod błędu: {response.status_code}")
        return {}


def get_all_acts_this_year(year=0):
    if year == 0:
        thisYear = datetime.now().year
    try:
        while (True):
            response = requests.get(
                f"http://api.sejm.gov.pl/eli/acts/DU/{year}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Błąd: {response.status_code}")
                return None
    except:
        print("błąd")


def is_the_new_act_in_effect_today():
    thisYear = datetime.now().year
    today = datetime.date(datetime.now())

    response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}")
    if response.status_code == 200:
        responsecount = response.json()
        var = responsecount.get('count', [])
        response = requests.get(
            f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}/{var}")

        resjson = response.json()
        if 'changeDate' in resjson:
            if (date.fromisoformat(resjson['changeDate'][0:10]) == today):
                return True
            else:
                return False


def get_titles_of_record(records):
    ustawy = []
    rozporzadzenia = []
    obwieszczenia = []

    items = records.get('items', [])[::-1]
    for record in items:
        act_type = record.get('type')  # Pobieramy typ aktu prawnego

        if act_type == 'Ustawa' and len(ustawy) < 10:
            ustawy.append(record['title'])
        elif act_type == 'Rozporządzenie' and len(rozporzadzenia) < 10:
            rozporzadzenia.append(record['title'])
        elif act_type == 'Obwieszczenie' and len(obwieszczenia) < 10:
            obwieszczenia.append(record['title'])

        if len(ustawy) == 10 and len(rozporzadzenia) == 10 and len(obwieszczenia) == 10:
            break

    return {
        'ustawy': ustawy,
        'rozporzadzenia': rozporzadzenia,
        'obwieszczenia': obwieszczenia
    }
