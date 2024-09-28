import requests
import datetime
from functools import wraps

def get_vote(term, sitting, id):
    response = requests.get(f'https://api.sejm.gov.pl/sejm/term{term}/votings/{sitting}/{id}')
    return response

def handle_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = kwargs.get('response')

        # If response is not provided, try extracting term, sitting, and id from args or kwargs
        if not response:
            if len(args) >= 3:
                term, sitting, id = args[:3]  # Positional arguments
            else:
                term = kwargs.get('term')
                sitting = kwargs.get('sitting')
                id = kwargs.get('id')
            
            # Ensure term, sitting, and id are provided
            if term is None or sitting is None or id is None:
                raise ValueError("Provide term, sitting, and id when response is not given")
            
            # Fetch the response
            response = get_vote(term, sitting, id)
            kwargs['response'] = response

        # Call the wrapped function with response
        return func(*args, **kwargs)
    
    return wrapper


@handle_response
def get_date(term=None, sitting=None, id=None, response=False):
    return datetime.datetime.strptime(response.json()['date'], '%Y-%m-%dT%H:%M:%S')

@handle_response
def get_votes_with_mode(term=None, sitting=None, id=None, mode=None, response=False):
    #abstain', 'date', 'kind', 'no', 'notParticipating', 'sitting', 'sittingDay', 'term', 'title', 'topic', 'totalVoted', 'votingNumber', 'yes'
    match mode:
        case "yes" | 0 | "za":
            return response.json()['yes']
        case "no" | 1 | "przeciw":
            return response.json()['no']
        case "abstain" | 2 | "wstrzymał":
            return response.json()['abstain']
        case "notParticipating" | 3 | "nieobecni":
            return response.json()['notParticipating']
        case "totalVoted" | 4 | "suma":
            return response.json()['totalVoted']
        case _:
            return response.json()['yes'] + " - " + response.json()['no'] + " - " + response.json()['abstain'] + response.json()['notParticipating']

@handle_response
def get_info(term=None, sitting=None, id=None, mode=None, response=False):
    match mode:
        case "votingNumber" | 0 | "nr_głosowania":
            return response.json()['votingNumber']
        case "sitting" | 1 | "nr_posiedzenia":
            return response.json()['sitting']
        case "title" | 2 | "punkt_obrad":
            return response.json()['title']
        case "topic" | 3 | "przedmiot":
            return response.json()['topic']
        case "kind" | 4 | "typ":
            return response.json()['kind']
        
# Using all arguments
date = get_date(10, 18, 1)
votes = get_votes_with_mode(10, 18, 1, 'yes')
info = get_info(10,18,1,'punkt_obrad')

print("===============")
print(date)
print(votes)
print(info)

# Using keyword arguments
date = get_date(term=10, sitting=18, id=1)
votes = get_votes_with_mode(term=10, sitting=18, id=1, mode='no')
info = get_info(term=10,sitting=18,id=1, mode="topic")

print("===============")
print(date)
print(votes)
print(info)

# Gotowa odpowiedź
response1 = get_vote(10,18,1)
date = get_date(response=response1)
votes = get_votes_with_mode(response=response1, mode='abstain')
info = get_info(response=response1, mode=0)

print("===============")
print(date)
print(votes)
print(info)