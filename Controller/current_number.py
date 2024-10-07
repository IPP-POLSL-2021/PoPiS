# By robić losowe opóźnienia. Niech ktoś się wypowie czy cringe czy dobry pomysł
import random
from time import sleep
import requests


# 21.08.2024 - Ostatnia kadencja sejmu miała numer 10
def get_term_number(current_term_number=10):
    # 1 kadencja Sejmu też nie zwraca nic XDDD
    erw = current_term_number
    while (True):
        response = requests.get(f'https://api.sejm.gov.pl/sejm/term{erw}')
        if response.status_code != 200:
            return erw-1
        erw += 1
        sleep(random.random()/10)


# 21.08.2024 - Ostatnie posiedzenie sejmu 10 kadencji miało numer 16
def get_sitting_number(term=get_term_number(), current_sitting_number=16):
    # 26.08.2024 Psikus się stał bo dodali 17 posiedzenie które jeszcze się nie odbyło ani nie jest w trakcie i nie ma opcji na sprawdzenia poza sprawdzeniem dat
    erw = current_sitting_number
    while (True):
        response = requests.get(
            f'https://api.sejm.gov.pl/sejm/term{term}/proceedings/{erw}')
        if response.status_code != 200:
            return erw-1
        erw += 1
        sleep(random.random()/10)


# 21.08.2024 - Ostatnie głosowanie 16 posiedzenia sejmu 10 kadencji miało numer 85
def get_voting_number(term=get_term_number(), sitting=get_sitting_number(), current_voting_number=85):
    erw = current_voting_number
    while (True):
        response = requests.get(
            f"https://api.sejm.gov.pl/sejm/term{term}/votings/{sitting}/{erw}")
        if response.status_code != 200:
            return erw-1
        erw += 1
        sleep(random.random()/100)


# Jeśli wywołujemy skrypt bezpośrednio
if __name__ == "__main__":
    term_number = get_term_number()
    sitting_number = get_sitting_number(term_number)
    voting_number = get_voting_number(term_number, sitting_number)
     print(
     f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu")
    # 26.08.2024 Expected Output Głosowanie nr 84 na 17 posiedzeniu 10 kadencji Sejmu
    # Tak zdaję sobie sprawę że to zdanie jest fałszywe ze względu na to że na 17 posiedzeniu nie było jeszcze żadnych głosowań bo jeszcze się nie zaczęło.
