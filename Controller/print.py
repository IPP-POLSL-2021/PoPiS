import requests
import datetime
from functools import wraps

def get_print(term, num):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/prints/{num}')         
    return response

# Enable supplying just response or full parameters
def handle_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = kwargs.get('response')

        # If response is not provided, try extracting term, sitting, and id from args or kwargs
        if not response:
            if len(args) >= 2:
                term, num = args[:2]  # Positional arguments
            else:
                term = kwargs.get('term')
                num = kwargs.get('num')
            
            # Ensure term, num are provided
            if term is None or num is None:
                raise ValueError("Provide term and num when response is not given")
            
            # Fetch the response
            response = get_print(term,num)
            kwargs['response'] = response

        # Call the wrapped function with response
        return func(*args, **kwargs)
    
    return wrapper

@handle_response
def get_title(term=None, num=None, response=False):
    return response.json()['title']

@handle_response
def get_date(term=None, num=None, mode=None, response=False):
    match mode:
        case 'document_date' | 0 | 'data_dokumentu' | 'date':
            return datetime.datetime.strptime(response.json()['documentDate'], '%Y-%m-%d').date()
        case 'change_date' | 1 | 'data_zmiany' | 'lastChange':
            return datetime.datetime.strptime(response.json()['changeDate'], '%Y-%m-%dT%H:%M:%S')
        case 'delivery_date' | 2 | 'data_otrzymania' | 'receivedDate':
            return datetime.datetime.strptime(response.json()['deliveryDate'], '%Y-%m-%d').date()
        case _:
            raise Exception("Mode must be specified")

# Mostly one pdf, sometimes additional "docx". Legally binding containing all info is only the pdf though
@handle_response
def get_attachment(term=None,num=None, response=False):
    return response.json()['attachments'] 

@handle_response
def get_related(term=None,num=None,response=False):
    try:
        return response.json()['additionalPrints']       
    except KeyError:
        return False
if __name__ == "__main__" :
    response = get_print(10,1)
    print(get_title(response=response))
    print(get_date(mode=0,response=response))
    print(get_related(response=response))
    #print(get_related(10,1,response))
