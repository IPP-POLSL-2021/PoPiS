# Robi za nas user-agent, headery, cookies itp generalnie sprawia że API nas chce
from api_for_polish_sejm_client import Client

# Typy danych tak jak string, int etc
from api_for_polish_sejm_client.types import Response
from api_for_polish_sejm_client.types import File

from api_for_polish_sejm_client.models import Interpellation

#from api_for_polish_sejm_client.api.default import get_sejm_termterm_interpellations_num_reply_key_body 
#from api_for_polish_sejm_client.api.default import get_sejm_termterm_interpellations_num_body
from api_for_polish_sejm_client.api.default import get_sejm_termterm_interpellations_num
#from api_for_polish_sejm_client.api.default import get_sejm_termterm_interpellations

#with Client(base_url="https://api.sejm.gov.pl") as client:
#response: Response[Term] = get_sejm_termterm.sync_detailed(term=erw, client=client)
#if not response.parsed:
# num should be str
def get_interpelation(term_number, interpelation_number):
    with Client(base_url="https://api.sejm.gov.pl") as client:
        response: Response[Interpellation] = get_sejm_termterm_interpellations_num.sync_detailed(term=term_number, num=interpelation_number, client=client)
        return response.parsed

def get_replies(response):
    urls = list()
    for i in response.replies:
        # i czyli response.parsed.replies.attachments może również zawierać ciało html. Trzeba będzie to sprawdać poprzez 
        for j in i.attachments:
            urls.append(j.url)
    return urls

#if __name__ == "__main__" :
    #with Client(base_url="https://api.sejm.gov.pl") as client:
        #response_single: Response[Interpellation] = get_sejm_termterm_interpellations_num.sync_detailed(term=10,num="3999", client=client)
        #response_multiple: Response[Interpellation] = get_sejm_termterm_interpellations_num.sync_detailed(term=10,num="296", client=client)
        #response_noanswer: Response[Interpellation] = get_sejm_termterm_interpellations_num.sync_detailed(term=10,num="1481", client=client)
        #D8AJ46
        #
        #CZRK2H
        #D29JSZ
        #D34L8A
        #
        # Empty Li
        #for i in response_single.parsed.replies:
        #    for j in i.attachments:
        #        print(j.url)
        #print("================")
        #for i in response_multiple.parsed.replies:
        #    for j in i.attachments:
        #        print(j.url)
        #print("================")
        #for i in response_noanswer.parsed.replies:
            # Jeśli nie ma odpowiedzi to ta pętla po prostu się kończy natychmiast
            # Pusta lista to false więc można if response_noanswer.parsed.replies
        #    print("1")
        #    for j in i.attachments:
        #        print(j.url)