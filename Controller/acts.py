import requests
from datetime import datetime, date



def get_all_acts_this_year():
    thisYear = datetime.now().year
    while (True):
        response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Błąd: {response.status_code}")
            return None

def did_today_new_ustawa_obowiazuje():
    thisYear = datetime.now().year
    today = datetime.date(datetime.now())

    response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}")
    if response.status_code == 200:
        responsecount = response.json()
        var = responsecount.get('count', [])
        response = requests.get(f"http://api.sejm.gov.pl/eli/acts/DU/{thisYear}/{var}")
            
            
        resjson = response.json()
        if 'changeDate' in resjson:
            if (date.fromisoformat(resjson['changeDate'][0:10])==today):
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

