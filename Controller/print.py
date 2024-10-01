import requests
import datetime

def get_print(term, num): # Przyjmuje numer kadencji i druku a zwraca odpowiedź w formie json
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/prints/{num}')         
    return response

def get_title(term, num, response=False):
    if not response:
        response = get_print(term,num)
    return response.json()['title']

def get_date(term, num, mode, response=False):
    if not response:
        response = get_print(term,num)
    match mode:
        case 'document_date' | 0 | 'data_dokumentu' | 'date':
            return datetime.datetime.strptime(response.json()['documentDate'], '%Y-%m-%d').date()
        case 'change_date' | 1 | 'data_zmiany' | 'lastChange':
            return datetime.datetime.strptime(response.json()['changeDate'], '%Y-%m-%dT%H:%M:%S')
        case 'delivery_date' | 2 | 'data_otrzymania' | 'receivedDate':
            return datetime.datetime.strptime(response.json()['deliveryDate'], '%Y-%m-%d').date()

# Mostly one pdf, sometimes additional "docx". Legally binding containing all info is only the pdf though
def get_attachment(term,num, response=False):
    if not response:
        response = get_print(term,num)
    return response.json()['attachments'] 

def get_related(term,num,response=False):
    if not response:
        response = get_print()
    try:
        return response.json()['additionalPrints']       
    except KeyError:
        return False
if __name__ == "__main__" :
    response = get_print(10,1)
    print(get_related(10,1,response))