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

# By robić losowe opóźnienia. Niech ktoś się wypowie czy cringe czy dobry pomysł
import random
from time import sleep

# Można by zrobić argumenty opcjonalnymi i wywoływać funkcje podległe 
# Done

def get_term_number(current_term_number=10): # 21.08.2024 - Ostatnia kadencja sejmu miała numer 10
    
    with Client(base_url="https://api.sejm.gov.pl") as client:
        # 1 kadencja Sejmu też nie zwraca nic XDDD
        erw=current_term_number
        while (True):
            response: Response[Term] = get_sejm_termterm.sync_detailed(term=erw, client=client)
            if not response.parsed:
                return erw-1
            erw+=1
            sleep(random.random()/10)

def get_sitting_number(term=get_term_number(), current_sitting_number=16): # 21.08.2024 - Ostatnie posiedzenie sejmu 10 kadencji miało numer 16
    with Client(base_url="https://api.sejm.gov.pl") as client:
        erw=current_sitting_number
        while(True):
            response: Response[Voting] = get_sejm_termterm_votings_sitting.sync_detailed(term=term, sitting=erw, client=client)
            if not response.parsed:
                return erw-1
            erw+=1
            sleep(random.random()/10)

def get_voting_number(term=get_term_number(), sitting=get_sitting_number(), current_voting_number=85): # 21.08.2024 - Ostatnie głosowanie 16 posiedzenia sejmu 10 kadencji miało numer 85
    with Client(base_url="https://api.sejm.gov.pl") as client: 
        erw=current_voting_number
        while(True):
            response: Response[VotingDetails] = get_sejm_termterm_votings_sitting_num.sync_detailed(term=term, sitting=sitting, client=client, num=erw)
            if not response.parsed:
                return erw-1
            erw+=1
            sleep(random.random()/100)
            
# Jeśli wywołujemy skrypt bezpośrednio
if __name__ == "__main__" :
    term_number=get_term_number()
    sitting_number=get_sitting_number(term_number)
    voting_number=get_voting_number(term_number,sitting_number)
    print(f"Głosowanie nr {voting_number} na {sitting_number} posiedzeniu {term_number} kadencji Sejmu")
