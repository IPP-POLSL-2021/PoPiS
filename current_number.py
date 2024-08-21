from time import sleep

# Robi za nas user-agent, headery, cookies itp generalnie sprawia że API nas chce
from api_for_polish_sejm_client import Client

# Typy danych tak jak string, int etc
from api_for_polish_sejm_client.types import Response

# Modele, tak też nie wiem co to jest, wygląda na to że element instancji typu danych np Voting zawiera się w Response
from api_for_polish_sejm_client.models import Term
from api_for_polish_sejm_client.models import Voting
from api_for_polish_sejm_client.models import VotingDetails

# Faktyczne funkcje
from api_for_polish_sejm_client.api.default import get_sejm_termterm
from api_for_polish_sejm_client.api.default import get_sejm_termterm_votings_sitting
from api_for_polish_sejm_client.api.default import get_sejm_termterm_votings_sitting_num

import random

# Można by zrobić argumenty opcjonalnymi i wywoływać funkcje podległe 

def get_term_number(client): # 21.08.2024 - Ostatnia kadencja sejmu miała numer 10
    with client as client:
        # 1 kadencja Sejmu też nie zwraca nic XDDD
        erw=2
        while (True):
            response: Response[Term] = get_sejm_termterm.sync_detailed(term=erw, client=client)
            if not response.parsed:
                return erw-1
            erw+=1
            sleep(random.random()/10)

def get_sitting_number(client,term): # 21.08.2024 - Ostatnie posiedzenie sejmu 10 kadencji miało numer 16
    with client as client:
        erw=1
        while(True):
            response: Response[Voting] = get_sejm_termterm_votings_sitting.sync_detailed(term=term, sitting=erw, client=client)
            if not response.parsed:
                return erw-1
            erw+=1
            sleep(random.random()/10)

def get_voting_number(client,term, sitting): # 21.08.2024 - Ostatnie głosowanie 16 posiedzenia sejmu 10 kadencji miało numer 85
    with client as client: 
        erw=1
        while(True):
            response: Response[VotingDetails] = get_sejm_termterm_votings_sitting_num.sync_detailed(term=term, sitting=sitting, client=client, num=erw)
            if not response.parsed:
                return erw-1
            erw+=1
            sleep(random.random()/100)
if __name__ == "__main__" :
    # Handler "with" zamyka Clienta którego nie da się ponownie otworzyć
    client = Client(base_url="https://api.sejm.gov.pl")
    term_number=get_term_number(client)
    client = Client(base_url="https://api.sejm.gov.pl")
    sitting_number=get_sitting_number(client,term_number)
    client = Client(base_url="https://api.sejm.gov.pl")
    voting_number=get_voting_number(client,term_number,sitting_number)
    print(f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu")